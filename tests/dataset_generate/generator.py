import argparse
import os

from third_party.runfiles import runfiles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--passphrase', required=True)
    parser.add_argument('--mode', required=True)
    options = parser.parse_args()

    assert options.passphrase == 'a b c', 'key is %r' % options.key

    # Make sure we have access to the data file.
    resolver = runfiles.Create()
    location = resolver.Rlocation('rules_contest/tests/dataset_generate/generator.data')
    assert location and os.path.exists(location), location

    out_dir = os.environ.get('OUTPUT_DIR')
    assert os.path.isdir(out_dir), 'OUTPUT_DIR does not exist'
    if options.mode == 'default':
        with open(os.path.join(out_dir, 'data1.in'), 'w'):
            pass
        with open(os.path.join(out_dir, 'data2.ans'), 'w'):
            pass
    elif options.mode == 'empty':
        pass
    else:
        assert False, '--mode=%s' % options.mode


if __name__ == '__main__':
    main()
