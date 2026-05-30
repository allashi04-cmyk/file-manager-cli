import os
import logging
from datetime import datetime

def add_date(args):
    path = args.path
    recursive = getattr(args, 'recursive', False)

    if not os.path.exists(path):
        raise FileNotFoundError(f" Путь не найден: {path}")

    if os.path.isfile(path):
        _process_file(path)
    elif os.path.isdir(path):
        _process_directory(path, recursive)
    else:
        raise ValueError(f" Неизвестный тип пути: {path}")

def _process_directory(directory, recursive):
    if recursive:
        # Рекурсивный обход всех вложенных папок
        for root, _, files in os.walk(directory):
            for file in files:
                _process_file(os.path.join(root, file))
    else:
        # Только файлы в текущей папке
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isfile(full_path):
                _process_file(full_path)

def _process_file(file_path):
    try:
        # Получаем время создания/изменения метаданных
        ctime = os.path.getctime(file_path)
        date_str = datetime.fromtimestamp(ctime).strftime("%Y-%m-%d")

        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        name, ext = os.path.splitext(base_name)

        new_name = f"{name}_{date_str}{ext}"
        new_path = os.path.join(dir_name, new_name)

        # Защита от повторного переименования
        if file_path == new_path:
            logging.debug(f" Дата уже добавлена: {base_name}")
            return

        if os.path.exists(new_path):
            raise FileExistsError(f" Файл уже существует: {new_path}")

        os.rename(file_path, new_path)
        logging.info(f" Переименовано: {base_name} -> {new_name}")
    except Exception as e:
        logging.error(f" Ошибка при обработке {file_path}: {e}")
        raise