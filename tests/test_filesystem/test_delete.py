import unittest
import os
import tempfile
import argparse
from filesystem.delete import delete_path


class TestDeletePath(unittest.TestCase):
    def test_delete_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test_file.txt")
            with open(file_path, "w") as f:
                f.write("data")

            args = argparse.Namespace(path=file_path)
            delete_path(args)

            self.assertFalse(os.path.exists(file_path))

    def test_delete_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dir_path = os.path.join(tmpdir, "test_dir")
            os.makedirs(os.path.join(dir_path, "subdir"))
            with open(os.path.join(dir_path, "file.txt"), "w") as f:
                f.write("data")

            args = argparse.Namespace(path=dir_path)
            delete_path(args)

            self.assertFalse(os.path.exists(dir_path))

    def test_delete_non_existent(self):
        args = argparse.Namespace(path="/tmp/this_path_does_not_exist_12345")
        with self.assertRaises(FileNotFoundError):
            delete_path(args)