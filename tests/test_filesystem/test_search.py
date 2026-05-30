import unittest
import os
import tempfile
import argparse
from filesystem.search import search_files


class TestSearchFiles(unittest.TestCase):
    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            args = argparse.Namespace(directory=tmpdir, pattern=r"\.txt$")
            self.assertEqual(search_files(args), [])

    def test_flat_matches(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            for name in ["a.txt", "b.log", "c.txt"]:
                open(os.path.join(tmpdir, name), "w").close()
            args = argparse.Namespace(directory=tmpdir, pattern=r"\.txt$")
            result = search_files(args)
            self.assertEqual(len(result), 2)
            self.assertTrue(all(path.endswith(".txt") for path in result))

    def test_nested_matches(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sub = os.path.join(tmpdir, "sub")
            os.makedirs(sub)
            open(os.path.join(tmpdir, "main.py"), "w").close()
            open(os.path.join(sub, "helper.py"), "w").close()
            open(os.path.join(sub, "data.txt"), "w").close()
            
            args = argparse.Namespace(directory=tmpdir, pattern=r"\.py$")
            result = search_files(args)
            self.assertEqual(len(result), 2)

    def test_invalid_regex(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            args = argparse.Namespace(directory=tmpdir, pattern="[invalid")
            with self.assertRaises(ValueError):
                search_files(args)