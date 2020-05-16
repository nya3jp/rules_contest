#!/usr/bin/python

import os
import random

MAX = 1000000000
seq = 0


def Generate(out_dir, a, b):
    global seq
    filename = '50-random%02d.in' % seq
    with open(os.path.join(out_dir, filename), 'w') as f:
        f.write('{} {}\n'.format(a, b))
    seq += 1


def main():
    out_dir = os.environ['OUTPUT_DIR']
    for _ in range(20):
        Generate(out_dir, random.randrange(0, MAX), random.randrange(0, MAX))


if __name__ == '__main__':
    main()
