# Building and Testing Solutions

This section describes how to build and test solutions using `rules_contest`.

## What is a solution?

A *solution* is a program that solves a programming contest problem.
To prepare programming contest problems, contest organizers typically write
two or more solutions to each problem. One of the solutions is used as
a *reference solution* to generate expected answers to test cases, and other
solutions are used to verify correctness of the solutions by comparing their
outputs.

## What is a judge?

A *judge* is a program that takes a solution program as an input and
evaluates it. Typically a judge has an associated dataset and runs a solution
program for each test case, but how to evaluate a solution is entirely up to
judges.

## Simple judge

In the most classical type of programming contest problems, a solution program
reads a test case from the standard input, writes an answer to the standard
output, and a judge compares the output with a reference solution's output to
determine if the solution is correct.

[`simple_judge`] rule generates a simple judge program from a dataset containing
inputs and answers, and optionally a *comparator* program. A simple judge runs
a solution for each test case and determines if a program output matches with
an answer by running the specified comparator program. If no comparator is
specified, [the default exact comparator] is used.

A simple judge optionally accepts a command line flag `--expect` that specifies
the expectation of a solution.

| Flag | Expectation |
| --- | --- |
| `--expect=accept_all` | A solution is accepted for all test cases (default) |
| `--expect=reject_any` | A solution is rejected for any one of test cases |
| `--expect=reject_all` | A solution is rejected for all test cases |

![simple_judge](../images/simple_judge.svg)

[`simple_judge`]: ../reference/rules.html#simple-judge
[the default exact comparator]: ../reference/targets.html#rules-contest-contest-fake-coverage-report-generator

## Testing solutions

[`solution_test`] is a test rule that runs a judge against a solution.
On executing a judge program, the path to the specified solution program is
passed as a command line argument. A test is considered pass if the judge
program exits normally (exit code 0). You can also specify extra arguments to
pass to the judge program to control a judge program's behavior.

![solution_test](../images/solution_test.svg)

[`solution_test`]: ../reference/rules.html#solution-test
