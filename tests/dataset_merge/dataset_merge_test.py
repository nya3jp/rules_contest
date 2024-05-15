import unittest
import zipfile


class DatasetMergeTest(unittest.TestCase):
    def test_dataset(self):
        with zipfile.ZipFile('tests/dataset_merge/dataset.zip') as zf:
            self.assertEqual(
                sorted(zf.namelist()),
                ['data1.in', 'data2.in', 'data3.ans', 'data3.in'])

    def test_empty(self):
        with zipfile.ZipFile('tests/dataset_merge/empty.zip') as zf:
            self.assertEqual(zf.namelist(), [])


if __name__ == '__main__':
    unittest.main()
