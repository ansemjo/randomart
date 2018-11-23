# randomart.py

A script to present SHAKE256 hashes as small ASCII-art pictures, similarly to OpenSSH's
[randomart](https://superuser.com/q/22535).

This allows easier verification by humans but may not be as secure as a bytewise comparison of the
digest!

<span style="display:block;text-align:center">![](assets/randomart.png)</span>

See the paper
["Hash Visualization: a New Technique to improve Real-World Security", Perrig A. and Song D., 1999, International Workshop on Cryptographic Techniques and E-Commerce (CrypTEC '99)](http://www.ece.cmu.edu/~adrian/projects/validation/validation.pdf)
for more information.

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
