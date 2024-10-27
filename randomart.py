#!/usr/bin/env python3

# Copyright (c) 2018 Anton Semjonov
# Licensed under the MIT License

import argparse, sys
from signal import signal, SIGINT

from random_art import metadata, crypto
from random_art.randomart import draw, drunkenwalk, TRANSLATION

# exit on ctrl-c
signal(SIGINT, lambda *a: sys.exit(1))

# initialize argument parser
parser = argparse.ArgumentParser(
    description=metadata.get("description"),
    epilog="%%(prog)s version %s" % metadata.get("version")
)

# the input file to be hashed
parser.add_argument("file",
    type=argparse.FileType("rb"),
    default=None,
    nargs="?",
    help="input file (default: stdin)",
)

# print frame in ascii characters
parser.add_argument("--ascii",
    action="store_true",
    help="use ascii frame",
)

# additionally display base64 encoded hash
parser.add_argument("--hash",
    action="store_true",
    help="print base64 encoded hash",
)

# parse commandline
args = parser.parse_args()

if args.file is None:  # no input file was specified
    import os
    if os.name == 'posix':  # Linux and macOS
        file = "/dev/stdin"
    elif os.name == 'nt':   # Windows
        import sys
        file = sys.stdin.buffer.raw

# hash the file
digest = crypto.digest(file)

# maybe print encoded digest
if args.hash:
    from base64 import b64encode
    print("%s:%s" % (crypto.HASHNAME, b64encode(digest).decode()))

# generate randomart
art = draw(drunkenwalk(digest), name=crypto.HASHNAME)

# maybe translate to ascii
if args.ascii:
    art = art.translate(TRANSLATION)

# print randomart
print(art, end="")
