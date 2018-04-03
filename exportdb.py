from tkinter import ttk
from tkinter.ttk import *

from tkinter import filedialog

import tkglobals as tkg
import tkinter as tk
import tkutils as tku

import sharing

class ExportDbScreen(ttk.Frame):
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

    self.title = ttk.Label(cont, text='Exportă baza de date')
    self.title.config(font=tkg.title_font())
    self.title.grid(row=0, column=0, sticky='w')

    self.path_label = ttk.Label(cont, textvariable=self.path)
    self.path_label.config(font=tkg.small_regular_font())
    self.path_label.config(wraplength=220, justify=tk.CENTER)
    self.path_label.grid(row=2, column=0, pady=(10, 0))

    self.label1 = ttk.Label(cont, text='Alege o parolă')
    self.label1.config(font=tkg.regular_font())
    self.label1.grid(row=3, column=0, sticky='w', pady=(15, 0))

    self.pass_entry1 = ttk.Entry(cont, show='*')
    self.pass_entry1.config(font=tkg.regular_font())
    self.pass_entry1.grid(row=4, column=0, sticky='ew', pady=(5, 0))

    self.label2 = ttk.Label(cont, text='Parolă (din nou)')
    self.label2.config(font=tkg.regular_font())
    self.label2.grid(row=5, column=0, sticky='w', pady=(10, 0))

    self.pass_entry2 = ttk.Entry(cont, show='*')
    self.pass_entry2.config(font=tkg.regular_font())
    self.pass_entry2.grid(row=6, column=0, sticky='ew', pady=(5, 0))

    self.error_label = tk.Label(cont, text='')
    self.error_label.config(font=tkg.small_regular_font(), fg='red')
    self.error_label.grid(row=7, column=0, pady=(10, 0))

  def place_button_gui(self):
    cont = self.container

    style = ttk.Style()
    style.configure('EDS.TButton', font=tkg.button_regular_font_tuple())

    self.choose_button = ttk.Button(cont, text='Alege numele fișierului')
    self.choose_button.config(style='EDS.TButton', command=self.choose_click)
    self.choose_button.grid(row=1, column=0, sticky='ew', pady=(30, 0))

    but_cont = ttk.Frame(cont)
    but_cont.grid(row=8, column=0)
    tku.prepare_centering(but_cont)

    but_cont2 = ttk.Frame(but_cont)
    but_cont2.grid(row=1, column=1, pady=(10, 0))

    self.back_button = ttk.Button(but_cont2, text='Înapoi')
    self.back_button.config(style='EDS.TButton', command=self.back_click)
    self.back_button.grid(row=0, column=0, padx=5)

    self.export_button = ttk.Button(but_cont2, text='Exportă')
    self.export_button.config(style='EDS.TButton', command=self.export_click)
    self.export_button.grid(row=0, column=1, padx=5)

  def choose_click(self):
    choice = filedialog.asksaveasfilename(title='Alege numele fișierului')
    if choice == '':
      return

    if not choice.endswith('.db'):
      choice += '.db'

    self.path.set(choice)

  def back_click(self):
    self.controller.show_user_menu_screen(self.us)

  def export_click(self):
    path = self.path.get()
    if path == '':
      self.error_label.config(text='Alege numele fișierului.')
      return

    pass1 = self.pass_entry1.get()
    pass2 = self.pass_entry2.get()
    if pass1 == '' or pass2 == '':
      self.error_label.config(text='Introdu parolele.')
      return

    if pass1 != pass2:
      self.error_label.config(text='Parolele nu corespund.')
      return

    sharing.export_database(self.us, path, pass1)
    self.error_label.config(text='Am creat fișierul.')

