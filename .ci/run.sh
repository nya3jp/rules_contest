#!/bin/bash

cd "$(dirname "$0")/.."

set -ex

cd example
bazel --bazelrc=../.ci/bazelrc test //...
