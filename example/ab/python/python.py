import sys


def solve(a, b):
    return a + b


def main():
    a, b = map(int, sys.stdin.read().strip().split())
    print(solve(a, b))


if __name__ == '__main__':
    main()
