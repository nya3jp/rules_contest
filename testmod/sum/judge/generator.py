import os
import random

from sum import constraints

seq = 0


def generate(out_dir, a, b):
    global seq
    filename = '50-random%02d.in' % seq
    with open(os.path.join(out_dir, filename), 'w') as f:
        f.write('{} {}\n'.format(a, b))
    seq += 1


def main():
    out_dir = os.environ['OUTPUT_DIR']
    random.seed(283)
    for _ in range(20):
        a = random.randrange(0, constraints.VALUE_MAX + 1)
        b = random.randrange(0, constraints.VALUE_MAX + 1)
        generate(out_dir, a, b)


if __name__ == '__main__':
    main()
