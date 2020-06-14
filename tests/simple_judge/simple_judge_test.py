import json
import os
import subprocess
import unittest

from bazel_tools.tools.python.runfiles import runfiles

resolver = runfiles.Create()

judge_path = resolver.Rlocation(
    'rules_contest/tests/simple_judge/judge')
good_solution_path = resolver.Rlocation(
    'rules_contest/tests/simple_judge/good_solution')
half_solution_path = resolver.Rlocation(
    'rules_contest/tests/simple_judge/half_solution')
bad_solution_path = resolver.Rlocation(
    'rules_contest/tests/simple_judge/bad_solution')


class SimpleJudgeTest(unittest.TestCase):
    maxDiff = None

    def test_results(self):
        subprocess.check_call([judge_path, good_solution_path])

        output_files = ['results.json'] + [
            'data%d.%s' % (i, suffix)
            for i in (1, 2)
            for suffix in (
                'solution.output',
                'solution.stdout',
                'solution.stderr',
                'judge.stdout',
                'judge.stderr',
            )]
        out_dir = os.environ['TEST_UNDECLARED_OUTPUTS_DIR']
        self.assertEqual(sorted(os.listdir(out_dir)), sorted(output_files))

        with open(os.path.join(out_dir, 'results.json')) as f:
            results = json.load(f)

        # Fix undeterministic fields.
        for case in results['cases']:
            case['time'] = 123456
            case['details'].update({
                'solution_time': 123456,
                'judge_time': 123456,
            })

        golden_path = resolver.Rlocation(
            'rules_contest/tests/simple_judge/results_golden.json')
        with open(golden_path) as f:
            golden = json.load(f)

        self.assertEqual(results, golden)

    def test_default(self):
        self.assertEqual(0, subprocess.call([judge_path, good_solution_path]))
        self.assertEqual(1, subprocess.call([judge_path, half_solution_path]))
        self.assertEqual(1, subprocess.call([judge_path, bad_solution_path]))

    def test_accept_all(self):
        self.assertEqual(0, subprocess.call([judge_path, '--expect=accept_all', good_solution_path]))
        self.assertEqual(1, subprocess.call([judge_path, '--expect=accept_all', half_solution_path]))
        self.assertEqual(1, subprocess.call([judge_path, '--expect=accept_all', bad_solution_path]))

    def test_reject_any(self):
        self.assertEqual(1, subprocess.call([judge_path, '--expect=reject_any', good_solution_path]))
        self.assertEqual(0, subprocess.call([judge_path, '--expect=reject_any', half_solution_path]))
        self.assertEqual(0, subprocess.call([judge_path, '--expect=reject_any', bad_solution_path]))

    def test_reject_all(self):
        self.assertEqual(1, subprocess.call([judge_path, '--expect=reject_all', good_solution_path]))
        self.assertEqual(1, subprocess.call([judge_path, '--expect=reject_all', half_solution_path]))
        self.assertEqual(0, subprocess.call([judge_path, '--expect=reject_all', bad_solution_path]))


if __name__ == '__main__':
    unittest.main()
