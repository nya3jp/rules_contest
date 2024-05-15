import unittest
import zipfile

from third_party.runfiles import runfiles

resolver = runfiles.Create()


class DatasetGenerateTest(unittest.TestCase):
    def test_dataset1(self):
        expects = {
            'data1.in': b'1\n',
            'data1.ans': b'11\n',
            'data2.in': b'2\n',
            'data2.ans': b'22\n',
        }

        zip_path = resolver.Rlocation(
            'rules_contest/tests/dataset_derive/dataset1.zip')

        with zipfile.ZipFile(zip_path) as zf:
            self.assertEqual(sorted(zf.namelist()), sorted(expects))
            for name, content in expects.items():
                with zf.open(name, 'r') as f:
                    self.assertEqual(f.read(), content)


if __name__ == '__main__':
    unittest.main()
