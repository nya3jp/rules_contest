import os
import tempfile
import unittest

from contest.impls.lib import datasets


class DatasetsTest(unittest.TestCase):

    def test_empty_dataset(self):
        with tempfile.NamedTemporaryFile() as zip_file:
            with tempfile.TemporaryDirectory() as empty_dir:
                datasets.create(empty_dir, zip_file.name)
            with datasets.expand(zip_file.name) as dataset_dir:
                self.assertEqual([], os.listdir(dataset_dir))


if __name__ == '__main__':
    unittest.main()
