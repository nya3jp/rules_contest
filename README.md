# rules_contest

rules_contest is a set of [Bazel] rules for maintaining programming contest problems.

This project started as an experiment to port [Rime] to Bazel rules.


## Trying the demo

1. Install [Bazel].
2. Run `bazel test //...` in the `example` directory.

```
$ cd example
$ bazel test //...
INFO: Analyzed 15 targets (26 packages loaded, 251 targets configured).
INFO: Found 12 targets and 3 test targets...
INFO: Elapsed time: 19.926s, Critical Path: 12.49s
INFO: 25 processes: 25 darwin-sandbox.
INFO: Build completed successfully, 84 total actions
//ab/cpp:cpp_test                                                        PASSED in 3.5s
//ab/cpp_WA:cpp_WA_test                                                  PASSED in 3.4s
//ab/python:python_test                                                  PASSED in 6.7s

Executed 3 out of 3 tests: 3 tests pass.
INFO: Build completed successfully, 84 total actions
```


[Bazel]: https://bazel.build/
[Rime]: https://github.com/icpc-jag/rime
