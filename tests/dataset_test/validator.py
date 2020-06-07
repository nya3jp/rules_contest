import sys


def main():
    if len(sys.argv) < 2:
        n = int(input())
    else:
        with open(sys.argv[1]) as f:
            n = int(f.read().strip())

    assert n % 2 == 0


if __name__ == '__main__':
    main()
