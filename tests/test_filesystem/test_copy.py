import unittest
import os
import tempfile
import argparse
from filesystem.copy import copy_file


class TestCopyFile(unittest.TestCase):
    def test_copy_success(self):
        # Создаём временную папку (автоматически удалится после теста)
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "source.txt")
            dst = os.path.join(tmpdir, "dest.txt")

            # 1. Создаём исходный файл
            with open(src, "w", encoding="utf-8") as f:
                f.write("Привет, это тестовый контент!")

            # 2. Имитируем объект args, который создаёт argparse
            args = argparse.Namespace(source=src, destination=dst)

            # 3. Запускаем нашу функцию
            copy_file(args)

            # 4. Проверяем результаты
            self.assertTrue(os.path.exists(dst), "Файл назначения не создан")
            with open(dst, "r", encoding="utf-8") as f:
                self.assertEqual(f.read(), "Привет, это тестовый контент!")