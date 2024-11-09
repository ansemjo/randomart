from io import StringIO
from numpy import zeros, array

def bytes_to_octal(bytestr):
    # calculate best possible number of digits
    digits = int(len(bytestr) * 8/3)
    # generate format string
    fmt = b"%%0%do" % digits
    # convert bytes to int and format as octal string
    octal = fmt % int.from_bytes(bytestr, byteorder='big')
    # return maximum "saturated" digits
    return octal[-digits:]

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
def drunkenwalk(digest, size=(9, 18)):
    # initialize "drawing board" and positional vector
    matrix = zeros(size).astype(int)
    position = (array(size) / 2).astype(int)
    # perform movements and compute matrix
    for move in movements(bytes_to_octal(digest)):
        p = tuple(position)
        matrix[p] += 1
        position = (position + move) % size
    return matrix

# character palette for drawing
PALETTE = " .*=%!~R_EWS0123456789abcdefghijklmnop"

# translation hash for ascii output
TRANSLATION = {
    ord("╭"): "/", ord("╮"): "\\", ord("╰"): "\\", ord("╯"): "/",
    ord("│"): "|", ord("─"): "-", ord("╴"): "[", ord("╶"): "]",
}

# draw characters in a box
def draw(matrix, name, palette=PALETTE):
    if len(name) != 10:
        raise ValueError("name must be 10 characters")
    # pick n'th character from palette
    symbol = lambda n: PALETTE[n % len(PALETTE)]
    # write randomart to string buffer line by line
    art = StringIO()
    art.write("╭──╴randomart.py╶──╮\n")
    for line in matrix:
        art.write("│%s│\n" % "".join((symbol(el) for el in line)))
    art.write("╰───╴%s╶───╯\n" % name)
    return art.getvalue()
