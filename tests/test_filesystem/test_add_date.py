import unittest
import os
import tempfile
import argparse
from filesystem.add_date import add_date


class TestAddDate(unittest.TestCase):
    def test_single_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "report.txt")
            open(file_path, "w").close()

            args = argparse.Namespace(path=file_path, recursive=False)
            add_date(args)

            files = os.listdir(tmpdir)
            self.assertEqual(len(files), 1)
            self.assertTrue(files[0].startswith("report_") and files[0].endswith(".txt"))

    def test_directory_non_recursive(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sub = os.path.join(tmpdir, "sub")
            os.makedirs(sub)
            open(os.path.join(tmpdir, "a.txt"), "w").close()
            open(os.path.join(sub, "b.txt"), "w").close()

            args = argparse.Namespace(path=tmpdir, recursive=False)
            add_date(args)

            root_files = os.listdir(tmpdir)
            self.assertTrue(any(f.startswith("a_") for f in root_files))
            # Файл в подпапке НЕ должен быть переименован
            self.assertIn("b.txt", os.listdir(sub))

    def test_directory_recursive(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sub = os.path.join(tmpdir, "sub")
            os.makedirs(sub)
            open(os.path.join(tmpdir, "a.txt"), "w").close()
            open(os.path.join(sub, "b.txt"), "w").close()

            args = argparse.Namespace(path=tmpdir, recursive=True)
            add_date(args)

            self.assertTrue(any(f.startswith("a_") for f in os.listdir(tmpdir)))
            self.assertTrue(any(f.startswith("b_") for f in os.listdir(sub)))

    def test_file_not_found(self):
        args = argparse.Namespace(path="/tmp/missing_file_123.txt", recursive=False)
        with self.assertRaises(FileNotFoundError):
            add_date(args)