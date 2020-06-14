#!/bin/bash

exec bazel run //tests/render_test_results:render_test_results_test -- --update
