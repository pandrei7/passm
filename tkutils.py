""" Contain utility functions related to tkinter. """

import tkinter as tk

def prepare_centering(cont):
  """ Prepare a container for centering.
  
  The outer rows and columns of the container receive equal weights.

  It is recommended that another container is placed at (1, 1) in cont.
  The content that needs to be centered should then be placed
  inside this inner container.

  Example:
  tkutils.prepare_centering(cont)

  inner = tkinter.Frame(cont)
  inner.grid(row=1, column=1)

  centered = tkinter.Label(inner, text='This is centered')
  centered.pack()
  """

  cont.grid_rowconfigure(0, weight=1)
  cont.grid_rowconfigure(2, weight=1)
  cont.grid_columnconfigure(0, weight=1)
  cont.grid_columnconfigure(2, weight=1)

