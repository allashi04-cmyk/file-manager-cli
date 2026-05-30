import os
import logging

def format_size(size_bytes):
    """Форматирует байты в читаемый вид: 244mb, 3gb и т.д."""
    if size_bytes == 0:
        return "0b"
    units = ["b", "kb", "mb", "gb", "tb"]
    unit_idx = 0
    size = float(size_bytes)
    while size >= 1024.0 and unit_idx < len(units) - 1:
        size /= 1024.0
        unit_idx += 1
    
    if size == int(size):
        return f"{int(size)}{units[unit_idx]}"
    return f"{size:.1f}{units[unit_idx]}"

def get_dir_size(path):
    """Рекурсивно считает размер всех файлов внутри папки."""
    total = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # Игнорируем симлинки и проверяем существование
                if os.path.exists(fp) and not os.path.islink(fp):
                    total += os.path.getsize(fp)
    except PermissionError:
        logging.warning(f" Нет прав доступа к содержимому: {path}")
    return total

def analyse(args):
    directory = args.directory

    if not os.path.exists(directory):
        raise FileNotFoundError(f" Путь не найден: {directory}")
    if not os.path.isdir(directory):
        raise NotADirectoryError(f" Указанный путь не является папкой: {directory}")

    items = []
    total_size = 0

    # Сканируем только элементы первого уровня (как в примере ТЗ)
    try:
        for entry in os.scandir(directory):
            if entry.is_file(follow_symlinks=False):
                size = entry.stat().st_size
                total_size += size
                items.append((entry.name, size))
            elif entry.is_dir(follow_symlinks=False):
                size = get_dir_size(entry.path)
                total_size += size
                items.append((entry.name, size))
    except PermissionError:
        logging.warning(" Нет прав доступа к некоторым элементам папки")

    # Сортируем по убыванию размера для наглядности
    items.sort(key=lambda x: x[1], reverse=True)

    # Вывод в консоль
    print(f"> full size: {format_size(total_size)}")
    for name, size in items:
        print(f"> - {name:<20} {format_size(size):>8}")