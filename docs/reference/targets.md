# Targets

## `@rules_contest//contest:render_test_results`

An executable that summarizes test results as a Markdown document.

The only argument should be a path to a [build event protocol] JSON file.
A rendered Markdown document is written to the standard output.

Example:

```console
bazel test --keep_going --build_event_json_file=build.jsonl //...
bazel run @rules_contest//contest:render_test_results -- $PWD/build.jsonl > $PWD/report.md
```

[build event protocol]: https://docs.bazel.build/versions/master/build-event-protocol.html

## `@rules_contest//contest:fake_coverage_report_generator`

An executable that does nothing.

This rule can be specified to the `--coverage_report_generator` flag to avoid
downloading heavy OpenJDK archives on running tests when Java is not used.

## `@rules_contest//contest:exact_comparator`

An example that runs the `diff` command to compare an output file and
an answer file.

This command essentially runs `diff -u "$2" "$3"`.
