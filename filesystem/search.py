import os
import re
import logging

def search_files(args):
    directory = args.directory
    pattern = args.pattern

    if not os.path.exists(directory):
        raise FileNotFoundError(f" Путь не найден: {directory}")
    if not os.path.isdir(directory):
        raise NotADirectoryError(f" Указанный путь не является папкой: {directory}")

    try:
        compiled_pattern = re.compile(pattern)
    except re.error as e:
        raise ValueError(f" Некорректное регулярное выражение: {e}")

    found_files = []
    # Рекурсивный обход всех вложенных папок
    for root, _, files in os.walk(directory):
        for file in files:
            if compiled_pattern.search(file):
                full_path = os.path.join(root, file)
                found_files.append(full_path)

    if found_files:
        logging.info(f" Найдено файлов: {len(found_files)}")
        for f in found_files:
            logging.info(f"  - {f}")
    else:
        logging.info(" Файлы не найдены.")

    return found_files