#!/usr/bin/env python3
import argparse
import logging
import sys
from filesystem.copy import copy_file
from filesystem.delete import delete_path
from filesystem.count import count_files
from filesystem.search import search_files
from filesystem.add_date import add_date

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    parser = argparse.ArgumentParser(description="CLI File System Manager")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Доступные команды")

    # copy
    p_copy = subparsers.add_parser("copy", help="Копировать файл")
    p_copy.add_argument("source", help="Исходный файл")
    p_copy.add_argument("destination", help="Куда копировать")
    p_copy.set_defaults(func=copy_file)

    # delete
    p_delete = subparsers.add_parser("delete", help="Удалить файл или папку")
    p_delete.add_argument("path", help="Путь к файлу/папке")
    p_delete.set_defaults(func=delete_path)

    # count
    p_count = subparsers.add_parser("count", help="Посчитать файлы в папке")
    p_count.add_argument("directory", help="Папка для подсчёта")
    p_count.set_defaults(func=count_files)

    # search
    p_search = subparsers.add_parser("search", help="Найти файлы по регулярному выражению")
    p_search.add_argument("directory", help="Где искать")
    p_search.add_argument("pattern", help="Регулярное выражение")
    p_search.set_defaults(func=search_files)

    # add-date
    p_date = subparsers.add_parser("add-date", help="Добавить дату создания в имя файла")
    p_date.add_argument("path", help="Файл или папка")
    p_date.add_argument("--recursive", action="store_true", help="Обрабатывать вложенные папки рекурсивно")
    p_date.set_defaults(func=add_date)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()