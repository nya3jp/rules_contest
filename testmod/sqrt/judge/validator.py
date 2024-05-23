import re
import sys

from sqrt import constraints


def main():
    m = re.match(r'^(\d+)\n$', sys.stdin.read())
    assert m, 'Does not match with regexp'
    a = int(m.groups()[0])
    assert 1 <= a <= constraints.VALUE_MAX, 'a out of range: %d' % a


if __name__ == '__main__':
    main()
