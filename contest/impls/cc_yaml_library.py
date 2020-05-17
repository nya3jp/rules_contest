import argparse

import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--input', required=True)
    options = parser.parse_args()

    with open(options.input, 'r') as f:
        vars = yaml.safe_load(f)

    with open(options.output, 'w') as f:
        for key, value in sorted(vars.items()):
            print('#define %s %r' % (key, value), file=f)


if __name__ == '__main__':
    main()
