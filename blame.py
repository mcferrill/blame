#!/usr/bin/env python

'''usage: blame <path>... [options]

Options:
    -a AUTHOR  Only show lines from AUTHOR (default: None)
    -t TYPES   File types to count [default: py,c,h]
'''

import re
import os
import subprocess

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import guess_lexer_for_filename
from termcolor import colored
import docopt


authors = []
COLORS = (
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
    'grey',
    'red',
)


def show_file(path, args):
    file_extension = os.path.splitext(path.lower())[1][1:]
    if file_extension not in args['-t'].split(','):
        return

    try:
        git_blame = subprocess.check_output(['git', 'blame', path],
                                            universal_newlines=True,
                                            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return

    print(os.path.abspath(path))

    authors_in_file = set()
    lines = []
    for line in git_blame.splitlines():
        author_timestamp = re.search('\([\s\w\-\:\-]+\)', line)
        author = author_timestamp[0][1:-29].strip()
        if author not in authors:
            authors.append(author)
        authors_in_file.add(author)

        if args.get('-a', None) and args.get('-a').lower() != author:
            continue

        code = line.split(') ')[1].rstrip()
        c = code.strip()
        if not c:
            continue
        elif c.startswith('//'):
            continue
        elif c.startswith('/*'):
            continue
        elif '*/' in c:
            continue
        elif c == '}':
            continue
        elif path.endswith('.py') and c.startswith('#'):
            continue

        code = highlight(code,
                         guess_lexer_for_filename(path, code),
                         Terminal256Formatter(style='gruvbox-dark'))
        lines.append((author, code.rstrip()))

    author_width = max(len(author) for author in authors_in_file) + 2
    for author, code in lines:
        color = COLORS[authors.index(author)]
        author = colored(author.ljust(author_width), color)
        print(author, code)



def main():
    args = docopt.docopt(__doc__)

    for path in args['<path>']:
        if os.path.isfile(path):
            show_file(path, args)
        else:
            for directory, subdirectory, files in os.walk(path):
                for file in files:
                    show_file(os.path.join(directory, file), args)


if __name__ == '__main__':
    main()
