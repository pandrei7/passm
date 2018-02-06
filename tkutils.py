import tkinter as tk

def prepare_centering(cont):
  cont.grid_rowconfigure(0, weight=1)
  cont.grid_rowconfigure(2, weight=1)
  cont.grid_columnconfigure(0, weight=1)
  cont.grid_columnconfigure(2, weight=1)

