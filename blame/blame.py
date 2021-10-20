#!/usr/bin/env python

'''usage: blame <path>[, <path>...] [options]

Options:
    -a AUTHOR  Only show lines from AUTHOR [default: None]
    -t TYPES   File types to count [default: c,h,py]
'''

import os
import subprocess

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import guess_lexer_for_filename
from termcolor import colored
import docopt


authors = []


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

    for line in git_blame.splitlines():
        if 'Micah Ferrill' in line:
            if args.get('-a').lower() == 'bob':
                continue
            author = colored('Micah'.ljust(7), 'green')
        elif 'bbaggerman' in line:
            if args.get('-a').lower() == 'micah':
                continue
            author = colored('Bob'.ljust(7), 'yellow')
        else:
            author = 'Unknown'.ljust(7)

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

        code = highlight(code,
                         guess_lexer_for_filename(path, code),
                         Terminal256Formatter(style='gruvbox-dark'))
        print(author, code.rstrip())


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
