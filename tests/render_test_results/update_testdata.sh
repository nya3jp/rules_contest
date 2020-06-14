#!/bin/bash

cd "$(dirname "$0")/../.."

readonly build_json=$(mktemp)
trap "rm -f ${build_json}" EXIT

set -x

readonly targets=$(bazel query 'attr("tags", "manual", kind(".*_test rule", //tests/render_test_results/subtests/...))')

bazel test --build_event_json_file="${build_json}" --keep_going ${targets}

rm -rf tests/render_test_results/testdata
mkdir -p tests/render_test_results/testdata

python3 tests/render_test_results/filter_build_jsonl.py < "${build_json}" > tests/render_test_results/testdata/build.jsonl
