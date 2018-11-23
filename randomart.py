#!/usr/bin/env python3

# Copyright (c) 2018 Anton Semjonov
# Licensed under the MIT License

from numpy import zeros, array
import hashlib

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

# digest a reader to produce pseudorandom data
# with length mod 3
digestsize = 54
def shake(reader):
  sha = hashlib.shake_256()
  while True:
    r = reader.read(4096)
    if not r:
      break
    sha.update(r)
  return sha.digest(digestsize)
  
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
def draw(mat, ascii=False):
  print("+--|randomart.py|--+" if ascii else "╭──╴randomart.py╶──╮")
  for line in mat:
    print("|" if ascii else "│", end="")
    print("".join((symbol(el) for el in line)), end="")
    print("|" if ascii else "│")
  print(("+---|SHAKE256/%d|--+" if ascii else "╰───╴SHAKE256/%d╶──╯") % digestsize)

# print base64 encoded hash
def printhash(H):
  import base64
  print("SHAKE256/%d:%s" % (digestsize, base64.b64encode(H).decode()))

# -----------
if __name__ == "__main__":

  import argparse
  import signal

  signal.signal(signal.SIGINT, lambda *a: exit(1))

  # type of an int divisible by 3
  def int3(arg):
    i = int(arg)
    if i % 3 != 0:
      raise argparse.ArgumentTypeError("argument not divisible by 3")
    return i

  parser = argparse.ArgumentParser()
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
  parser.add_argument(
      "--digest-size",
      help="SHAKE256 digest size (must be divisible by 3)",
      default=54,
      type=int3,
      metavar="bytes",
  )
  args = parser.parse_args()

  digestsize = args.digest_size
  digest = shake(args.file)

  if args.hash:
    printhash(digest)
  draw(randomart(digest), args.ascii)
