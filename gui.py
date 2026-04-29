# gui.py
import flet as ft # type: ignore
import os
import types
import logging
from filesystem.copy import copy_file
from filesystem.delete import delete_path
from filesystem.count import count_files
from filesystem.search import search_files
from filesystem.add_date import add_date
from filesystem.analyse import analyse

COMMANDS = {
    "copy": {"label": " Копировать", "fields": ["source", "destination"], "tooltips": ["Исходный файл", "Куда копировать"], "types": ["file", "file_or_dir"], "func": copy_file},
    "delete": {"label": " Удалить", "fields": ["path"], "tooltips": ["Путь к файлу/папке"], "types": ["file_or_dir"], "func": delete_path},
    "count": {"label": " Подсчитать", "fields": ["directory"], "tooltips": ["Папка для подсчёта"], "types": ["dir"], "func": count_files},
    "search": {"label": " Поиск", "fields": ["directory", "pattern"], "tooltips": ["Где искать", "Регулярное выражение"], "types": ["dir", "text"], "func": search_files},
    "add-date": {"label": " Добавить дату", "fields": ["path", "recursive"], "tooltips": ["Файл или папка", "Обработать вложенные папки рекурсивно?"], "types": ["file_or_dir", "checkbox"], "func": add_date},
    "analyse": {"label": " Анализ", "fields": ["directory"], "tooltips": ["Папка для анализа размера"], "types": ["dir"], "func": analyse},
}
  
def main(page: ft.Page):
    try:
        page.show_error_banner = False
    except AttributeError:
        pass
    
    page.title = " File System Manager GUI"
    page.window_width = 850
    page.window_height = 750
    page.padding = 20
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.scroll = ft.ScrollMode.AUTO 
    page.show_error_banner = False 
       
    # Файловые пикеры
    pick_file = ft.FilePicker()
    pick_dir = ft.FilePicker()
    page.overlay.extend([pick_file, pick_dir])

    output_area = ft.Text(value=" Выбери команду и нажми «Запустить»", size=14, selectable=True)
    command_buttons = ft.Row(wrap=True, spacing=10)
    form_container = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO)
    ui_fields = {}
    current_command = None
    active_picker_target = None

    def show_snack(msg, color= "#53935"):
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=color, open=True)
        page.update()

    def on_file_result(e):
        if e.files and e.files[0]:
            active_picker_target.value = e.files[0].path
            page.update()

    def on_dir_result(e):
        if e.path:
            active_picker_target.value = e.path
            page.update()

    pick_file.on_result = on_file_result
    pick_dir.on_result = on_dir_result

    def rebuild_form(cmd_key):
        nonlocal current_command, form_container, ui_fields, active_picker_target
        current_command = cmd_key
        form_container.controls.clear()
        ui_fields.clear()
        active_picker_target = None

        cfg = COMMANDS[cmd_key]
        for i, field in enumerate(cfg["fields"]):
            if cfg["types"][i] == "checkbox":
                ui_fields[field] = ft.Checkbox(label=cfg["tooltips"][i], value=False)
                form_container.controls.append(ui_fields[field])
            else:
                tf = ft.TextField(label=cfg["tooltips"][i], tooltip=cfg["tooltips"][i], expand=True, read_only=(cfg["types"][i] != "text"))
                ui_fields[field] = tf
                active_picker_target = tf

                btn = ft.IconButton(
                    icon="folder_open",
                    tooltip="Выбрать через системный пикер",
                    on_click=lambda e, t=cfg["types"][i]: (pick_dir.get_directory_path() if t == "dir" else pick_file.pick_files(allow_multiple=False))
                )
                form_container.controls.append(ft.Row([tf, btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
        page.update()

    def execute_command(e):
        if not current_command:
            show_snack(" Сначала выбери команду")
            return
        cfg = COMMANDS[current_command]
        args_data = {}
        for field in cfg["fields"]:
            ui = ui_fields[field]
            args_data[field] = ui.value if not isinstance(ui, ft.Checkbox) else ui.value

        for i, field in enumerate(cfg["fields"]):
            if cfg["types"][i] != "checkbox" and not args_data.get(field):
                show_snack(f" Заполните поле: {cfg['tooltips'][i]}")
                return

        try:
            args = types.SimpleNamespace(**args_data)
            cfg["func"](args)
            output_area.value = " Команда выполнена успешно!"
        except FileNotFoundError as err:
            output_area.value = f" Файл/папка не найдены: {err}"
        except PermissionError as err:
            output_area.value = f" Нет прав на операцию: {err}"
        except Exception as err:
            output_area.value = f" Ошибка выполнения: {err}"
            logging.error(f"GUI Error: {err}", exc_info=True)
        page.update()

    for key, cfg in COMMANDS.items():
        btn = ft.ElevatedButton(cfg["label"], on_click=lambda e, k=key: rebuild_form(k), tooltip=cfg["label"])
        command_buttons.controls.append(btn)

    rebuild_form("copy")

    page.add(
        ft.Column([
            ft.Text(" File System Manager", size=26, weight="bold", text_align=ft.TextAlign.CENTER),
            ft.Text("Выберите инструмент:", size=14, weight="bold", color="#616161"),
            command_buttons,
            ft.Divider(),
            form_container,
            ft.ElevatedButton(" Запустить", on_click=execute_command, bgcolor="#1976d2", color="white", width=220, height=40),
            ft.Divider(),
            ft.Container(
                content=ft.Column([
                    ft.Text(" Результат / Логи:", weight="bold", size=14),
                    ft.Container(content=output_area, padding=12, bgcolor="#f5f5f5", border_radius=8, border=ft.border.all(1, "#e0e0e0"), expand=True)
                ], spacing=8),
                expand=True
            )
        ], spacing=16, expand=True)
    )

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER, port=8080)