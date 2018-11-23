# randomart.py

[![CodeFactor](https://www.codefactor.io/repository/github/ansemjo/randomart/badge)](https://www.codefactor.io/repository/github/ansemjo/randomart)

A script to present SHAKE256 hashes as small ASCII-art pictures, similarly to OpenSSH's
[randomart](https://superuser.com/q/22535).

This allows easier verification by humans but may not be as secure as a bytewise comparison of the
digest!

<span style="display:block;text-align:center">![](assets/randomart.png)</span>

See the paper [Hash Visualization: a New Technique to improve Real-World Security<sup>1</sup>][^1]
for more information on the concept of random art.

The paper [The drunken bishop: An analysis of the OpenSSH fingerprint visualization
algorithm<sup>2</sup>][^2] analyses the OpenSSH implementation in more detail.

It should be explicitly noted that my algorithm is _similar_ but not _identical_ to the "drunken
bishop" walk of the OpenSSH implementation. The implementation at hand:

- flips sides at the borders, which turns the field into a torus
- moves in all possible directions with distance 1, not only diagonally
- does not mark start (`S`) and end (`E`) and uses a different character palette

I have not performed any similar analysis[<sup>2</sup>][^2] but would expect my implementation to
perform no worse.

## usage

Use `--help` to output up-to-date usage help. The following arguments are available:

- `--ascii` - use only ASCII characters for the box frame
- `--hash` - print the computed digest before the randomart picture
- `--digest-size <bytes>` - use a different digest size with SHAKE256

The data to be digested is read either from the file given as the first positional argument or
standard input if none was given.

Internally, the data is hashed twice: the first digest is used to print the digest in base64 encoded
form. This digest ist then hashed itself to produce the input for the randomart. This is done so
that small differences in the computed digest result in vastly different pictures. The digest size
must be divisble by 3 due to the use of three-bit values to generate movements on the "drawing
board".

[^1]:
  http://www.ece.cmu.edu/~adrian/projects/validation/validation.pdf
  "Perrig A. and Song D., 1999, International Workshop on Cryptographic Techniques and E-Commerce
  (CrypTEC '99)"

[^2]:
  http://www.dirk-loss.de/sshvis/drunken_bishop.pdf
  "Dirk Loss, Tobias Limmer, Alexander von Gernler, 2009"
