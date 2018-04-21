import os
import sys

def get_base_path():
  if getattr(sys, 'frozen', False):
    return sys._MEIPASS
  return os.path.dirname(os.path.abspath(__file__))


def get_resource_path(resource):
  return os.path.join(get_base_path(), resource)
