import sys


def main():
    # Bazel's handling of args is weird.
    # https://docs.bazel.build/versions/master/be/common-definitions.html#binary.args
    expect = [
        'a', 'b',  # segmented by a space
        'c d', 'e f',  # quotes are recognized
        'g', 'h',  # spaces are trimmed
        # empty strings are omitted
        '--',
        '',  # can pass an empty argument by quotes
        '',
        '""',  # quotes can be escaped by backslashes
        '\'\'',
        '$HOME',  # environment variables are not substituted
        '||', 'true',  # pipelines are not recognized
    ]
    print('Expect: %r' % expect)
    print('Actual: %r' % sys.argv[1:])
    if sys.argv[1:] != expect:
        print('FAIL!')
        sys.exit(1)
    print('OK')


if __name__ == '__main__':
    main()
