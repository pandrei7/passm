""" Contain functions for the EsoCrypt algorithm. """

import random

def random_uppercase():
  """ Return a random uppercase ASCII letter. """
  return chr(ord('A') + random.randint(0, 25))


def random_lowercase():
  """ Return a random lowercase ASCII letter. """
  return chr(ord('a') + random.randint(0, 25))


def random_bool():
  """ Return a random boolean. """
  return random.choice([True, False])


def offset_char(ch, offset):
  """ Offset a character by a certain amount. 
  
  If offset is a positive value, the character gets shifted forwards,
  and if it is negative, the character gets shifted backwards.
  """
  left_end = ord(' ')
  right_end = ord('~')
  num = ord(ch) + offset

  if num < left_end:
    num = right_end - (left_end - num) + 1
  if num > right_end:
    num = left_end + (num - right_end) - 1
  return chr(num)


def encrypt(data):
  """ Encrypt data using the EsoCrypt algorithm. """
  step = 6
  offset = 0
  encrypted = random_uppercase() if random_bool() else random_lowercase()

  for i in range(len(data)):
    if i % step == 0:
      offset = random.randint(1, 9)
      encrypted += chr(ord('0') + offset)

    if random_bool():
      encrypted += random_uppercase()
      encrypted += offset_char(data[i], offset)
    else:
      encrypted += random_lowercase()
      encrypted += offset_char(data[i], -offset)

  return encrypted


def decrypt(data):
  """ Decrypt data using the EsoCrypt algorithm. """
  step = 6
  countdown = 0
  offset = 0
  decrypted = ''

  index = 1
  while index < len(data):
    if countdown == 0:
      offset = int(data[index])
      index += 1
      countdown = step

    if data[index].isupper():
      decrypted += offset_char(data[index + 1], -offset)
    else:
      decrypted += offset_char(data[index + 1], offset)

    index += 2
    countdown -= 1

  return decrypted

