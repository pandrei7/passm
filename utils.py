import os
import sys

def get_base_path():
  if getattr(sys, 'frozen', False):
    return sys._MEIPASS
  return os.path.dirname(os.path.abspath(__file__))


def get_resource_path(*tokens):
  path = get_base_path()
  for tok in tokens:
    path = os.path.join(path, tok)
  return path
  
