""" Contain utility function for general use. """

import os
import sys

def get_base_path():
  """ Return the application path. """
  if getattr(sys, 'frozen', False):
    return sys._MEIPASS
  return os.path.dirname(os.path.abspath(__file__))


def get_resource_path(*tokens):
  """ Get the full path of a resource.

  The tokens describe the sequence of directories/files that
  is appended to the base path to reach the resource.
  """
  path = get_base_path()
  for tok in tokens:
    path = os.path.join(path, tok)
  return path
  
