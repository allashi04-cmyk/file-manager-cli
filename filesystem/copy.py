import os
import shutil
import logging

def copy_file(args):
    src = args.source
    dst = args.destination

    if not os.path.exists(src):
        raise FileNotFoundError(f" Исходный файл не найден: {src}")

    # Если указан каталог, копируем файл внутрь него
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))

    shutil.copy2(src, dst)
    logging.info(f" Успешно скопировано: {src} -> {dst}")
    