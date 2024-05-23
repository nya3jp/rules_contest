import os
import random

from sqrt import constraints


def main():
    out_dir = os.environ['OUTPUT_DIR']
    random.seed(283)
    for i in range(20):
        with open(os.path.join(out_dir, '50-random%02d.in' % i), 'w') as f:
            a = random.randrange(1, constraints.VALUE_MAX + 1)
            print('%d' % a, file=f)


if __name__ == '__main__':
    main()
