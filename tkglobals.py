from tkinter import font

def regular_font():
  return font.Font(family='Helvetica', size=14)

def regular_font_tuple():
  return ('Helvetica', 14)


def small_regular_font():
  return font.Font(family='Helvetica', size=10)

def small_regular_font_tuple():
  return ('Helvetica', 10)


def bold_regular_font():
  return font.Font(family='Helvetica', size=14, weight='bold')

def bold_regular_font_tuple():
  return ('Helvetica', 14, 'bold')


def button_regular_font():
  return font.Font(family='Helvetica', size=12)

def button_regular_font_tuple():
  return ('Helvetica', 12)


def button_bold_regular_font():
  return font.Font(family='Helvetica', size=12, weight='bold')

def button_bold_regular_font_tuple():
  return ('Helvetica', 12, 'bold')


def title_font():
  return font.Font(family='Helvetica', size=18, weight='bold')

def title_font_tuple():
  return ('Helvetica', 18, 'bold')


def hyper_title_font():
  return font.Font(family='Helvetica', size=22, weight='bold')

def hyper_title_font_tuple():
  return ('Helvetica', 22, 'bold')
