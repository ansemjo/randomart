import numpy
import hashlib

# split every 3 bytes
def split3(bytearr):
  if len(bytearr) % 3 != 0:
    raise ValueError("length of 'bytearr' not divisible by 3")
  return (bytearr[i:i+3] for i in range(0, len(bytearr), 3))

# convert three bytes to a large int
# and split that into three-bit values {0..7}
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

# digest a reader to produce pseudorandom data mod 3
def sha384(reader):
  sha = hashlib.sha384()
  while True:
    r = reader.read(4096)
    if not r:
      break
    sha.update(r)
  return sha.digest()
  
# compute randomart matrix from data
def randomart(data):
  # initialize "drawing board" and positional vector
  size = (9,18)
  mat = numpy.zeros(size).astype(int)
  pos = (numpy.array(size) / 2).astype(int)
  # perform movements and compute matrix
  for mov in movements(sha384(data)):
    p = tuple(pos)
    mat.itemset(p, mat.item(p) + 1)
    pos = (pos + mov) % size
  return mat

# character palette for display
palette = " `*=%!REWS"
#palette = " .aBcDeFgHiJkLmNoPqRsT"
symbol = lambda c: palette[ c % len(palette) ]
  
# draw characters in a box
def draw(mat):
  print("╭──╴randomart.py╶──╮")
  for line in mat:
    print("│", end='')
    print(''.join((symbol(el) for el in line)), end='')
    print("│")
  print("╰─────╴SHA384╶─────╯")

# -----------
if __name__ == '__main__':
  import sys
  draw(randomart(sys.stdin.buffer))
