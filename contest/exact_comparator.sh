#!/bin/sh

exec diff -u --label OUTPUT --label ANSWER "$2" "$3"
