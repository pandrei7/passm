from tkinter import ttk
from tkinter.ttk import *

from tkinter import filedialog

import tkglobals as tkg
import tkinter as tk
import tkutils as tku

from cryptography.fernet import InvalidToken

import sharing

class ImportDbScreen(ttk.Frame):
  def __init__(self, parent, us):
    ttk.Frame.__init__(self, parent)
    self.controller = parent
    self.us = us

    tku.prepare_centering(self)

    self.container = ttk.Frame(self)
    self.container.grid(row=1, column=1, sticky='nsew', pady=(30, 0))

    self.path = tk.StringVar()
    self.path.set('')

    self.place_main_gui()
    self.place_button_gui()

  def place_main_gui(self):
    cont = self.container

    self.title = ttk.Label(cont, text='Importă o bază de date')
    self.title.config(font=tkg.title_font())
    self.title.grid(row=0, column=0, sticky='w')

    self.path_label = ttk.Label(cont, textvariable=self.path)
    self.path_label.config(font=tkg.small_regular_font())
    self.path_label.config(wraplength=230, justify=tk.CENTER)
    self.path_label.grid(row=2, column=0, pady=(10, 0))

    self.label = ttk.Label(cont, text='Introdu parola')
    self.label.config(font=tkg.regular_font())
    self.label.grid(row=3, column=0, sticky='w', pady=(15, 0))

    self.pass_entry = ttk.Entry(cont, show='*')
    self.pass_entry.config(font=tkg.regular_font())
    self.pass_entry.grid(row=4, column=0, sticky='ew', pady=(5, 0))

    self.error_label = tk.Label(cont, text='')
    self.error_label.config(font=tkg.small_regular_font(), fg='red')
    self.error_label.grid(row=5, column=0, pady=(10, 0))

  def place_button_gui(self):
    cont = self.container

    style = ttk.Style()
    style.configure('IDS.TButton', font=tkg.button_regular_font_tuple())

    self.choose_button = ttk.Button(cont, text='Alege fișierul')
    self.choose_button.config(style='IDS.TButton', command=self.choose_click)
    self.choose_button.grid(row=1, column=0, sticky='ew', pady=(30, 0))

    but_cont = ttk.Frame(cont)
    but_cont.grid(row=6, column=0)
    tku.prepare_centering(but_cont)

    but_cont2 = ttk.Frame(but_cont)
    but_cont2.grid(row=1, column=1, pady=(10, 0))

    self.back_button = ttk.Button(but_cont2, text='Înapoi')
    self.back_button.config(style='IDS.TButton', command=self.back_click)
    self.back_button.grid(row=0, column=0, padx=5)

    self.import_button = ttk.Button(but_cont2, text='Importă')
    self.import_button.config(style='IDS.TButton', command=self.import_click)
    self.import_button.grid(row=0, column=1, padx=5)

  def choose_click(self):
    choice = filedialog.askopenfilename(title='Alege baza de date', filetypes=[('Bază de date', '*.db')])
    if choice == '':
      return

    self.path.set(choice)    

  def back_click(self):
    self.controller.show_user_menu_screen(self.us)

  def import_click(self):
    path = self.path.get()
    if path == '':
      self.error_label.config(text='Alege baza de date.')
      return

    password = self.pass_entry.get()
    if password == '':
      self.error_label.config(text='Introdu parola.')
      return

    try:
      sharing.import_database(self.us, path, password)
      self.error_label.config(text='Am importat baza de date cu succes.')
    except InvalidToken:
      self.error_label.config(text='Parolă incorectă.')

