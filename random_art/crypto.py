from hashlib import blake2b

# used hash algorithm
HASH = blake2b
HASHNAME = "BLAKE2b/64"

# chunksize for reading and updating
CHUNKSIZE = 64 * 1024

# update a hash in chunks and return digest
def digest(reader):
  h = HASH()
  while True:
    buf = reader.read(CHUNKSIZE)
    if not buf:
      break
    h.update(buf)
  return h.digest()
