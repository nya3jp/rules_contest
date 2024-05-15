import unittest
import zipfile


class DatasetGenerateTest(unittest.TestCase):
    def test_dataset(self):
        with zipfile.ZipFile('tests/dataset_generate/dataset.zip') as zf:
            self.assertEqual(
                sorted(zf.namelist()),
                ['data1.in', 'data2.ans'])

    def test_empty(self):
        with zipfile.ZipFile('tests/dataset_generate/empty.zip') as zf:
            self.assertEqual(zf.namelist(), [])


if __name__ == '__main__':
    unittest.main()
