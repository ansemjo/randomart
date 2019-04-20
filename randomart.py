#!/usr/bin/env python3

# Copyright (c) 2018 Anton Semjonov
# Licensed under the MIT License

import argparse

from randomart import metadata, randomart, crypto

# exit on ctrl-c
from signal import signal, SIGINT
signal(SIGINT, lambda *a: exit(1))

# initialize argument parser
parser = argparse.ArgumentParser(
    description=metadata.get("description"),
    epilog="%%(prog)s version %s" % metadata.get("version")
)
parser.add_argument("file", type=argparse.FileType("rb"), default="/dev/stdin", nargs="?", help="input file (default: stdin)")
parser.add_argument("--ascii", action="store_true", help="use ascii frame")
parser.add_argument("--hash", action="store_true", help="print base64 encoded hash line aswell")
args = parser.parse_args()

digest = crypto.digest(args.file)

if args.hash:
    from base64 import b64encode
    print("%s:%s" % (crypto.HASHNAME, b64encode(digest).decode()))

art = randomart.draw(randomart.randomwalk(digest), name=crypto.HASHNAME)
if args.ascii:
    art = art.translate(randomart.TRANSLATION)
print(art, end='')
