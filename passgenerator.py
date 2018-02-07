from tkinter import ttk
from tkinter.ttk import *

import tkglobals as tkg
import tkinter as tk

import platform

import clipbutton
import hidebutton
import secrets

class PassGeneratorFrame(ttk.Frame):
  def __init__(self, parent):
    ttk.Frame.__init__(self, parent)
    self.parent = parent

    self.place_main_gui()
    self.place_scale_gui()
    self.place_check_gui()
    self.place_entry_gui()
    self.place_button_gui()

  def place_main_gui(self):
    title = ttk.Label(self, text='Generează o parolă')
    title.config(font=tkg.title_font())
    title.grid(row=0, column=0, sticky='w', padx=(10, 0), pady=5)

  def place_scale_gui(self):
    label1 = ttk.Label(self, text='Alege lungimea parolei')
    label1.config(font=tkg.regular_font())
    label1.grid(row=1, column=0, sticky='w', padx=(10, 0), pady=(5, 0))

    self.scale = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL)
    self.scale.config(length=(432 if platform.system() == 'Windows' else 482))
    self.scale.grid(row=2, column=0, padx=5, pady=5)

  def place_check_gui(self):
    label2 = ttk.Label(self, text='Include')
    label2.config(font=tkg.regular_font())
    label2.grid(row=3, column=0, sticky='w', padx=(10, 0), pady=5)

    style = ttk.Style()
    style.configure('PGF.TCheckbutton', font=tkg.regular_font())

    check_cont = ttk.Frame(self)
    check_cont.grid(row=4, column=0, sticky='ew', padx=5, pady=5)

    self.use_lower = tk.IntVar()
    self.lower = ttk.Checkbutton(check_cont, text='Minuscule')
    self.lower.config(style='PGF.TCheckbutton', variable=self.use_lower)
    self.lower.grid(row=0, column=0, padx=5, pady=5)

    self.use_upper = tk.IntVar()
    self.upper = ttk.Checkbutton(check_cont, text='Majuscule')
    self.upper.config(style='PGF.TCheckbutton', variable=self.use_upper)
    self.upper.grid(row=0, column=1, padx=5, pady=5)

    self.use_digits = tk.IntVar()
    self.digits = ttk.Checkbutton(check_cont, text='Cifre')
    self.digits.config(style='PGF.TCheckbutton', variable=self.use_digits)
    self.digits.grid(row=0, column=2, padx=5, pady=5)

    self.use_punct = tk.IntVar()
    self.punct = ttk.Checkbutton(check_cont, text='Punctuație')
    self.punct.config(style='PGF.TCheckbutton', variable=self.use_punct)
    self.punct.grid(row=0, column=3, padx=5, pady=5)

  def place_entry_gui(self):
    entry_cont = ttk.Frame(self, width=432, height=40)
    if platform.system() != 'Windows':
      entry_cont.config(width=482)
    entry_cont.pack_propagate(False)
    entry_cont.grid(row=5, column=0, sticky='ew', padx=5, pady=5)

    self.entry = ttk.Entry(entry_cont)
    self.entry.config(font=tkg.regular_font())
    self.entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 3))

    self.hide_button = hidebutton.HideButton(entry_cont, self.entry)
    self.hide_button.pack(side=tk.LEFT, padx=(2, 3))

    self.clip_button = clipbutton.ClipButton(entry_cont, self.entry)
    self.clip_button.pack(side=tk.LEFT, padx=(2, 0))

  def place_button_gui(self):
    style = ttk.Style()
    style.configure('PGF.TButton', font=tkg.regular_font())

    self.button = ttk.Button(self, text='Generează')
    self.button.config(command=self.click, style='PGF.TButton')
    self.button.grid(row=6, column=0, padx=(10, 0), pady=5)

  def click(self):
    lower = (self.use_lower.get() == 1)
    upper = (self.use_upper.get() == 1)
    digits = (self.use_digits.get() == 1)
    punct = (self.use_punct.get() == 1)

    password = secrets.random_password(self.scale.get(),
                lower=lower, upper=upper, digits=digits, punct=punct)

    self.entry.delete(0, tk.END)
    self.entry.insert(0, password)
