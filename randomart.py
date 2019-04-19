#!/usr/bin/env python3

# Copyright (c) 2018 Anton Semjonov
# Licensed under the MIT License

from randomart import metadata
from numpy import zeros, array
from hashlib import blake2b

# split every 3 bytes
def split3(bytearr):
  if len(bytearr) % 3 != 0:
    raise ValueError("length of 'bytearr' not divisible by 3")
  return (bytearr[i : i + 3] for i in range(0, len(bytearr), 3))

# convert three bytes to a large int and
# split that into three-bit values {0..7}
def bits(triplet):
  if len(triplet) != 3:
    raise ValueError("length of 'triplet' not 3")
  concat = (triplet[0] << 16) + (triplet[1] << 8) + triplet[2]
  return [concat >> sh & 7 for sh in range(0, 24, 3)]

# associate values {0..7} with matrix movements
directions = {
    4:(-1,-1), 5:(-1, 0), 6:(-1, 1),
    3:( 0,-1),            7:( 0, 1),
    2:( 1,-1), 1:( 1, 0), 0:( 1, 1),
  }

# get a generator of movements in matrix
def movements(H):
  return (directions[i] for l in (bits(t) for t in split3(H)) for i in l)

# must follow hashlib library api and produce 64+ byte digest
HASH = blake2b

# read data in chunks
CHUNKSIZE = 64 * 1024

# digest a reader in chunks to produce pseudorandom data
def digest(reader):
  h = HASH()
  while True:
    buf = reader.read(4096)
    if len(buf) == 0:
      break
    h.update(buf)
  return h.digest()

# compute randomart matrix from hash
def randomart(H):
  # initialize "drawing board" and positional vector
  size = (9, 18)
  mat = zeros(size).astype(int)
  pos = (array(size) / 2).astype(int)
  # perform movements and compute matrix
  for mov in movements(H):
    p = tuple(pos)
    mat.itemset(p, mat.item(p) + 1)
    pos = (pos + mov) % size
  return mat

# character palette for display
palette = " .*=%!~R_EWS0123456789abcdefghijklmnop"
symbol = lambda c: palette[c % len(palette)]
  
# draw characters in a box
def draw(mat, use_ascii=False):
  print("+--|randomart.py|--+" if use_ascii else "╭──╴randomart.py╶──╮")
  for line in mat:
    print("|" if use_ascii else "│", end="")
    print("".join((symbol(el) for el in line)), end="")
    print("|" if use_ascii else "│")
  print(("+---|BLAKE2b/64|---+" if use_ascii else "╰───╴BLAKE2b/64╶───╯"))

# print base64 encoded hash
def printhash(H):
  import base64
  print("BLAKE2b/64:%s" % base64.b64encode(H).decode())

# -----------
if __name__ == "__main__":

  import argparse
  import signal

  signal.signal(signal.SIGINT, lambda *a: exit(1))

  parser = argparse.ArgumentParser(
    description=metadata.get("description"),
    epilog="%%(prog)s version %s" % metadata.get("version"),
  )
  parser.add_argument(
      "file",
      type=argparse.FileType("rb"),
      default="/dev/stdin",
      nargs="?",
      help="input file (default: stdin)",
  )
  parser.add_argument(
      "--ascii",
      action="store_true",
      help="use ASCII frame",
  )
  parser.add_argument(
      "--hash",
      action="store_true",
      help="print base64 encoded hash line aswell",
  )
  args = parser.parse_args()

  d = digest(args.file)

  if args.hash:
    printhash(d)
  draw(randomart(d[:63]), args.ascii)
