from tkinter import font

def regular_font():
  return font.Font(family='Helvetica', size=14)


def small_regular_font():
  return font.Font(family='Helvetica', size=10)


def title_font():
  return font.Font(family='Helvetica', size=18, weight='bold')


def hyper_title_font():
  return font.Font(family='Helvetica', size=22, weight='bold')
