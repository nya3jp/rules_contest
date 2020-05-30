import sys

from tests.example.sqrt import constraints


def main():
    _, out_file, ans_file = sys.argv[1:]
    with open(out_file, 'r') as f:
        a = float(f.read().strip())
    with open(ans_file, 'r') as f:
        b = float(f.read().strip())
    diff = abs(a - b)
    print('diff = %.10f' % diff)
    assert diff <= constraints.ERROR_MAX


if __name__ == '__main__':
    main()
