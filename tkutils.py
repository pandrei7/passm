import tkinter as tk

def prepare_centering(container):
  container.grid_rowconfigure(0, weight=1)
  container.grid_rowconfigure(2, weight=1)
  container.grid_columnconfigure(0, weight=1)
  container.grid_columnconfigure(2, weight=1)

