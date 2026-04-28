import unittest
import os
import tempfile
import argparse
import io
import sys
from filesystem.analyse import analyse, format_size


class TestAnalyse(unittest.TestCase):
    def test_format_size(self):
        self.assertEqual(format_size(0), "0b")
        self.assertEqual(format_size(512), "512b")
        self.assertEqual(format_size(1024), "1kb")
        self.assertEqual(format_size(1024 * 1024), "1mb")
        self.assertEqual(format_size(1024**3), "1gb")

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            args = argparse.Namespace(directory=tmpdir)
            captured = io.StringIO()
            sys.stdout = captured
            analyse(args)
            sys.stdout = sys.__stdout__
            self.assertIn("> full size: 0b", captured.getvalue())

    def test_mixed_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Файл 2MB
            with open(os.path.join(tmpdir, "big.dat"), "wb") as f:
                f.write(b"x" * (2 * 1024 * 1024))
            
            # Папка с файлом 1MB
            subdir = os.path.join(tmpdir, "my_folder")
            os.makedirs(subdir)
            with open(os.path.join(subdir, "data.bin"), "wb") as f:
                f.write(b"y" * (1 * 1024 * 1024))

            args = argparse.Namespace(directory=tmpdir)
            captured = io.StringIO()
            sys.stdout = captured
            analyse(args)
            sys.stdout = sys.__stdout__

            output = captured.getvalue()
            self.assertIn("full size: 3mb", output)
            self.assertIn("big.dat", output)
            self.assertIn("my_folder", output)

    def test_invalid_path(self):
        args = argparse.Namespace(directory="/tmp/nonexistent_test_123")
        with self.assertRaises(FileNotFoundError):
            analyse(args)