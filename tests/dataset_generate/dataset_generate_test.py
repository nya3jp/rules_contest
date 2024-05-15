import unittest
import zipfile

from third_party.runfiles import runfiles

resolver = runfiles.Create()


class DatasetGenerateTest(unittest.TestCase):
    def test_dataset(self):
        zip_path = resolver.Rlocation(
            'rules_contest/tests/dataset_generate/dataset.zip')
        with zipfile.ZipFile(zip_path) as zf:
            self.assertEqual(
                sorted(zf.namelist()),
                ['data1.in', 'data2.ans'])

    def test_empty(self):
        zip_path = resolver.Rlocation(
            'rules_contest/tests/dataset_generate/empty.zip')
        with zipfile.ZipFile(zip_path) as zf:
            self.assertEqual(zf.namelist(), [])


if __name__ == '__main__':
    unittest.main()
