import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--passphrase', required=True)
    parser.add_argument('--mode', required=True)
    options = parser.parse_args()

    assert options.passphrase == 'a b c', 'key is %r' % options.key

    out_dir = os.environ.get('OUTPUT_DIR')
    assert os.path.isdir(out_dir), 'OUTPUT_DIR does not exist'
    if options.mode == 'default':
        with open(os.path.join(out_dir, 'data1.in'), 'w'):
            pass
        with open(os.path.join(out_dir, 'data2.ans'), 'w'):
            pass


if __name__ == '__main__':
    main()
