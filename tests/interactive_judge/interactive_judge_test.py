import json
import os
import subprocess
import unittest

from third_party.runfiles import runfiles

resolver = runfiles.Create()

judge_path = resolver.Rlocation(
    'rules_contest/tests/interactive_judge/judge')
judge_with_runfiles_path = resolver.Rlocation(
    'rules_contest/tests/interactive_judge/judge_with_runfiles')
solution_good_path = resolver.Rlocation(
    'rules_contest/tests/interactive_judge/solution_good')
solution_half_path = resolver.Rlocation(
    'rules_contest/tests/interactive_judge/solution_half')
solution_bad_path = resolver.Rlocation(
    'rules_contest/tests/interactive_judge/solution_bad')
solution_slow_path = resolver.Rlocation(
    'rules_contest/tests/interactive_judge/solution_slow')
solution_with_runfiles_path = resolver.Rlocation(
    'rules_contest/tests/interactive_judge/solution_with_runfiles')


class InteractiveJudgeTest(unittest.TestCase):
    def test_results(self):
        subprocess.check_call([judge_path, solution_good_path])

        output_files = ['results.json'] + [
            'data%d.%s' % (i, suffix)
            for i in (1, 2)
            for suffix in ('solution.stderr', 'judge.stderr')]
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
            'rules_contest/tests/interactive_judge/results_golden.json')
        with open(golden_path) as f:
            golden = json.load(f)

        self.assertEqual(results, golden)

    def test_runfiles(self):
        self.assertEqual(0, subprocess.call([judge_with_runfiles_path, solution_with_runfiles_path]))

    def test_default(self):
        self.assertEqual(0, subprocess.call([judge_path, solution_good_path]))
        self.assertEqual(1, subprocess.call([judge_path, solution_half_path]))
        self.assertEqual(1, subprocess.call([judge_path, solution_bad_path]))
        self.assertEqual(1, subprocess.call([judge_path, solution_slow_path]))

    def test_accept_all(self):
        self.assertEqual(0, subprocess.call([judge_path, '--expect=accept_all', solution_good_path]))
        self.assertEqual(1, subprocess.call([judge_path, '--expect=accept_all', solution_half_path]))
        self.assertEqual(1, subprocess.call([judge_path, '--expect=accept_all', solution_bad_path]))
        self.assertEqual(1, subprocess.call([judge_path, '--expect=accept_all', solution_slow_path]))

    def test_reject_any(self):
        self.assertEqual(1, subprocess.call([judge_path, '--expect=reject_any', solution_good_path]))
        self.assertEqual(0, subprocess.call([judge_path, '--expect=reject_any', solution_half_path]))
        self.assertEqual(0, subprocess.call([judge_path, '--expect=reject_any', solution_bad_path]))
        self.assertEqual(0, subprocess.call([judge_path, '--expect=reject_any', solution_slow_path]))

    def test_reject_all(self):
        self.assertEqual(1, subprocess.call([judge_path, '--expect=reject_all', solution_good_path]))
        self.assertEqual(1, subprocess.call([judge_path, '--expect=reject_all', solution_half_path]))
        self.assertEqual(0, subprocess.call([judge_path, '--expect=reject_all', solution_bad_path]))
        self.assertEqual(1, subprocess.call([judge_path, '--expect=reject_all', solution_slow_path]))

    def test_timeout_any(self):
        self.assertEqual(1, subprocess.call([judge_path, '--expect=timeout_any', solution_good_path]))
        self.assertEqual(1, subprocess.call([judge_path, '--expect=timeout_any', solution_half_path]))
        self.assertEqual(1, subprocess.call([judge_path, '--expect=timeout_any', solution_bad_path]))
        self.assertEqual(0, subprocess.call([judge_path, '--expect=timeout_any', solution_slow_path]))


if __name__ == '__main__':
    unittest.main()
