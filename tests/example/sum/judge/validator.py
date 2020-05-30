import re
import sys

from tests.example.sum import constraints


def main():
    m = re.match(r'^(\d+) (\d+)\n$', sys.stdin.read())
    assert m, 'Does not match with regexp'
    a, b = map(int, m.groups())
    assert 0 <= a <= constraints.VALUE_MAX, 'a out of range: %d' % a
    assert 0 <= b <= constraints.VALUE_MAX, 'a out of range: %d' % b


if __name__ == '__main__':
    main()
