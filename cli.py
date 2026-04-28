#!/usr/bin/env python3
import argparse
import logging
import sys
from filesystem.copy import copy_file
from filesystem.delete import delete_path
from filesystem.count import count_files

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    parser = argparse.ArgumentParser(description="CLI File System Manager")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Доступные команды")

    # Команда copy
    p_copy = subparsers.add_parser("copy", help="Копировать файл")
    p_copy.add_argument("source", help="Исходный файл")
    p_copy.add_argument("destination", help="Куда копировать (файл или папка)")
    p_copy.set_defaults(func=copy_file)

    # Команда delete
    p_delete = subparsers.add_parser("delete", help="Удалить файл или папку")
    p_delete.add_argument("path", help="Путь к файлу или папке")
    p_delete.set_defaults(func=delete_path)

    # Команда count
    p_count = subparsers.add_parser("count", help="Посчитать количество файлов в папке")
    p_count.add_argument("directory", help="Папка для подсчёта")
    p_count.set_defaults(func=count_files)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()