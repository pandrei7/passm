from tkinter import ttk
from tkinter.ttk import *

import secrets
import tkglobals as tkg
import tkinter as tk

class PassGeneratorFrame(ttk.Frame):
  def __init__(self, parent):
    ttk.Frame.__init__(self, parent)
    self.parent = parent

    style = ttk.Style()

    title = ttk.Label(self, text='Generează o parolă')
    title.config(font=tkg.title_font())
    title.grid(row=0, column=0, sticky='w', padx=(10, 0), pady=5)

    label1 = ttk.Label(self, text='Alege lungimea parolei')
    label1.config(font=tkg.regular_font())
    label1.grid(row=1, column=0, sticky='w', padx=(10, 0), pady=(5, 0))

    self.scale = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL)
    self.scale.config(length=500)
    self.scale.grid(row=2, column=0, padx=5, pady=5)

    label2 = ttk.Label(self, text='Include')
    label2.config(font=tkg.regular_font())
    label2.grid(row=3, column=0, sticky='w', padx=(10, 0), pady=5)

    style.configure('PGF.TCheckbutton', font=tkg.regular_font())
    check_container = ttk.Frame(self)
    check_container.grid(row=4, column=0, sticky='ew', padx=5, pady=5)

    self.use_lower = tk.IntVar()
    self.lower = ttk.Checkbutton(check_container, text='Minuscule')
    self.lower.config(style='PGF.TCheckbutton', variable=self.use_lower)
    self.lower.grid(row=0, column=0, padx=5, pady=5)

    self.use_upper = tk.IntVar()
    self.upper = ttk.Checkbutton(check_container, text='Majuscule')
    self.upper.config(style='PGF.TCheckbutton', variable=self.use_upper)
    self.upper.grid(row=0, column=1, padx=5, pady=5)

    self.use_digits = tk.IntVar()
    self.digits = ttk.Checkbutton(check_container, text='Cifre')
    self.digits.config(style='PGF.TCheckbutton', variable=self.use_digits)
    self.digits.grid(row=0, column=2, padx=5, pady=5)

    self.use_punct = tk.IntVar()
    self.punct = ttk.Checkbutton(check_container, text='Punctuație')
    self.punct.config(style='PGF.TCheckbutton', variable=self.use_punct)
    self.punct.grid(row=0, column=3, padx=5, pady=5)

    entry_container = ttk.Frame(self, width=500, height=40)
    entry_container.pack_propagate(False)
    entry_container.grid(row=5, column=0, sticky='ew', padx=5, pady=5)

    self.entry = ttk.Entry(entry_container)
    self.entry.config(font=tkg.regular_font())
    self.entry.pack(fill=tk.BOTH)

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
