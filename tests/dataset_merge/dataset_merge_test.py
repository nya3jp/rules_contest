import unittest
import zipfile

from third_party.runfiles import runfiles

resolver = runfiles.Create()


class DatasetMergeTest(unittest.TestCase):
    def test_dataset(self):
        zip_path = resolver.Rlocation(
            'rules_contest/tests/dataset_merge/dataset.zip')
        with zipfile.ZipFile(zip_path) as zf:
            self.assertEqual(
                sorted(zf.namelist()),
                ['data1.in', 'data2.in', 'data3.ans', 'data3.in'])

    def test_empty(self):
        zip_path = resolver.Rlocation(
            'rules_contest/tests/dataset_merge/empty.zip')
        with zipfile.ZipFile(zip_path) as zf:
            self.assertEqual(zf.namelist(), [])


if __name__ == '__main__':
    unittest.main()
