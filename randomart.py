#!/usr/bin/env python3

# Copyright (c) 2018 Anton Semjonov
# Licensed under the MIT License

from randomart import metadata
from numpy import zeros, array
from hashlib import blake2b

def bytes_to_octal(bytestr):
  # calculate best possible number of digits
  digits = int(len(bytestr) * 8/3)
  # generate format string
  fmt = b"%%0%do" % digits
  # convert bytes to int and format as octal string
  octal = fmt % int.from_bytes(bytestr, byteorder='big')
  # return maximum "saturated" digits
  return octal[-digits:]

def directions(bytestr):
  # associate octal digit with movement vector
  dirhash = {
      ord('4'):(-1,-1), ord('5'):(-1, 0), ord('6'):(-1, 1),
      ord('3'):( 0,-1),                   ord('7'):( 0, 1),
      ord('2'):( 1,-1), ord('1'):( 1, 0), ord('0'):( 1, 1),
  }
  # return generator mapping each digit
  return (dirhash[c] for c in bytestr)

# update hash in chunks and digest
def digest(reader):
  h = blake2b()
  while True:
    buf = reader.read(64 * 1024)
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
  for mov in directions(bytes_to_octal(H)):
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
  draw(randomart(d), args.ascii)
