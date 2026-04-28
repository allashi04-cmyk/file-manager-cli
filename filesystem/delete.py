import os
import shutil
import logging

def delete_path(args):
    path = args.path

    if not os.path.exists(path):
        raise FileNotFoundError(f" Путь не найден: {path}")

    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
            logging.info(f" Папка успешно удалена: {path}")
        else:
            os.remove(path)
            logging.info(f" Файл успешно удален: {path}")
    except PermissionError:
        raise PermissionError(f" Нет прав на удаление: {path}")
    except Exception as e:
        raise RuntimeError(f" Ошибка при удалении {path}: {e}")