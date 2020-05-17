import argparse

import markdown

_EXTENSIONS = (
    'markdown.extensions.fenced_code',
    'markdown.extensions.tables',
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--input', required=True)
    options = parser.parse_args()

    with open(options.input, 'r') as f:
        text = f.read()

    html = markdown.markdown(text, extensions=_EXTENSIONS)

    with open(options.output, 'w') as f:
        f.write(html)


if __name__ == '__main__':
    main()
