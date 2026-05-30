import unittest
import os
import tempfile
import argparse
from filesystem.count import count_files


class TestCountFiles(unittest.TestCase):
    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            args = argparse.Namespace(directory=tmpdir)
            self.assertEqual(count_files(args), 0)

    def test_flat_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            for name in ["a.txt", "b.txt", "script.py"]:
                open(os.path.join(tmpdir, name), "w").close()
            args = argparse.Namespace(directory=tmpdir)
            self.assertEqual(count_files(args), 3)

    def test_nested_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sub = os.path.join(tmpdir, "subfolder")
            os.makedirs(os.path.join(sub, "deep"))
            
            open(os.path.join(tmpdir, "root.txt"), "w").close()
            open(os.path.join(sub, "level1.txt"), "w").close()
            open(os.path.join(sub, "deep", "level2.txt"), "w").close()
            
            args = argparse.Namespace(directory=tmpdir)
            self.assertEqual(count_files(args), 3)

    def test_invalid_path_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "not_a_dir.txt")
            open(file_path, "w").close()
            args = argparse.Namespace(directory=file_path)
            with self.assertRaises(NotADirectoryError):
                count_files(args)