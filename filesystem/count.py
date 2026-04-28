import os
import logging

def count_files(args):
    directory = args.directory
    
    if not os.path.exists(directory):
        raise FileNotFoundError(f" Путь не найден: {directory}")
    if not os.path.isdir(directory):
        raise NotADirectoryError(f" Указанный путь не является папкой: {directory}")

    file_count = 0
    # os.walk рекурсивно обходит все вложенные папки
    for root, dirs, files in os.walk(directory):
        file_count += len(files)

    logging.info(f" Найдено файлов: {file_count} в папке '{directory}'")
    return file_count