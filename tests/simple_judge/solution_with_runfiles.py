import os

from third_party.runfiles import runfiles


def main():
    # Make sure we have access to the data file.
    resolver = runfiles.Create()
    location = resolver.Rlocation('rules_contest/tests/simple_judge/solution.data')
    assert location and os.path.exists(location), location

    print(int(input()) * 42)


if __name__ == '__main__':
    main()
