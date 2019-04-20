from numpy import zeros, array
from io import StringIO

from .util import bytes_to_octal
from .crypto import HASHNAME

def movements(octal):
  # associate octal digit with movement vector
  directions = {
      ord('4'):(-1,-1), ord('5'):(-1, 0), ord('6'):(-1, 1),
      ord('3'):( 0,-1),                   ord('7'):( 0, 1),
      ord('2'):( 1,-1), ord('1'):( 1, 0), ord('0'):( 1, 1),
  }
  # return generator mapping each digit
  return (directions[c] for c in octal)

# compute randomart matrix from hash digest
def randomart(digest):
  # initialize "drawing board" and positional vector
  size = (9, 18)
  matrix = zeros(size).astype(int)
  position = (array(size) / 2).astype(int)
  # perform movements and compute matrix
  for move in movements(bytes_to_octal(digest)):
    p = tuple(position)
    matrix.itemset(p, matrix.item(p) + 1)
    position = (position + move) % size
  return matrix

# character palette for display
PALETTE = " .*=%!~R_EWS0123456789abcdefghijklmnop"
symbol = lambda c: PALETTE[c % len(PALETTE)]
  
# draw characters in a box
def draw(matrix, use_ascii=False):
  art = StringIO()
  # write randomart to string buffer line by line
  art.write("╭──╴randomart.py╶──╮\n")
  for line in matrix:
    art.write("│%s│\n" % "".join((symbol(el) for el in line)))
  art.write("╰───╴%s╶───╯\n" % HASHNAME)
  if use_ascii:
    # utf8 border to ascii translation
    return art.getvalue().translate({
      ord("╭"): "/", ord("╮"): "\\", ord("╰"): "\\", ord("╯"): "/",
      ord("│"): "|", ord("─"): "-", ord("╴"): "[", ord("╶"): "]", })
  return art.getvalue()