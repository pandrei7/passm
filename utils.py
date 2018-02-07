import os
import sys

def get_base_path():
  if getattr(sys, 'frozen', False):
    return sys._MEIPASS
  return os.path.dirname(os.path.abspath(__file__))

