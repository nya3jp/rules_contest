# Unit Tests

| Target | | Message |
| --- | --- | --- |
| //tests/render_test_results/subtests:bad_test | 🔥 | FAILED |
| //tests/render_test_results/subtests:good_test | 🍀 | PASSED |
# Solution Tests

| Target | | Message |
| --- | --- | --- |
| //tests/render_test_results/subtests/A:solution_accept_all_test | 🍀 | All accepted |
| //tests/render_test_results/subtests/A:solution_reject_any_test | 🔥 | All accepted unexpectedly |
| //tests/render_test_results/subtests/B:solution_accept_all_test | 🔥 | data2: Judge exited with code 1 |
| //tests/render_test_results/subtests/B:solution_reject_any_test | 🍀 | Rejected as expected: data2: Judge exited with code 1 |
# Solution Details

## //tests/render_test_results/subtests/A:judge

| Test case | solution_accept_all_test | solution_reject_any_test |
| --- | --- | --- |
| **data1** | 0.0s | 0.0s |
| **data2** | 0.0s | 0.0s |
## //tests/render_test_results/subtests/B:judge

| Test case | solution_accept_all_test | solution_reject_any_test |
| --- | --- | --- |
| **data1** | 0.0s | 0.0s |
| **data2** | Judge exited with code 1 | Judge exited with code 1 |
