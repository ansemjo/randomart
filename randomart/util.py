def bytes_to_octal(bytestr):
  # calculate best possible number of digits
  digits = int(len(bytestr) * 8/3)
  # generate format string
  fmt = b"%%0%do" % digits
  # convert bytes to int and format as octal string
  octal = fmt % int.from_bytes(bytestr, byteorder='big')
  # return maximum "saturated" digits
  return octal[-digits:]