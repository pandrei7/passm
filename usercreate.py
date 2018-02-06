from tkinter import ttk
from tkinter.ttk import *

import tkglobals as tkg
import tkinter as tk
import tkutils as tku

import accountdb
import user
import userdb

class UserCreateScreen(ttk.Frame):
  def __init__(self, parent):
    ttk.Frame.__init__(self, parent)
    self.controller = parent

    tku.prepare_centering(self)

    self.container = ttk.Frame(self)
    self.container.grid(row=1, column=1, sticky='nsew', pady=(30, 0))
    tku.prepare_centering(self.container)

    self.place_main_gui()
    self.place_button_gui()

  def place_main_gui(self):
    cont = self.container

    self.title = ttk.Label(cont, text='Creează cont nou')
    self.title.config(font=tkg.title_font())
    self.title.grid(row=0, column=0, sticky='w')

    self.label1 = ttk.Label(cont, text='Utilizator')
    self.label1.config(font=tkg.regular_font())
    self.label1.grid(row=1, column=0, sticky='w', pady=(30, 0))

    self.user_entry = ttk.Entry(cont)
    self.user_entry.config(font=tkg.regular_font())
    self.user_entry.grid(row=2, column=0, sticky='ew', pady=(5, 0))

    self.label2 = ttk.Label(cont, text='Parolă')
    self.label2.config(font=tkg.regular_font())
    self.label2.grid(row=3, column=0, sticky='w', pady=(10, 0))

    self.pass_entry1 = ttk.Entry(cont, show='*')
    self.pass_entry1.config(font=tkg.regular_font())
    self.pass_entry1.grid(row=4, column=0, sticky='ew', pady=(5, 0))

    self.label3 = ttk.Label(cont, text='Parolă (din nou)')
    self.label3.config(font=tkg.regular_font())
    self.label3.grid(row=5, column=0, sticky='w', pady=(10, 0))

    self.pass_entry2 = ttk.Entry(cont, show='*')
    self.pass_entry2.config(font=tkg.regular_font())
    self.pass_entry2.grid(row=6, column=0, sticky='ew', pady=(5, 0))

    self.error_label = tk.Label(cont, text='')
    self.error_label.config(font=tkg.small_regular_font(), fg='red')
    self.error_label.grid(row=7, column=0, pady=(10, 0))

  def place_button_gui(self):
    cont = self.container

    but_cont = ttk.Frame(cont)
    but_cont.grid(row=8, column=0)
    tku.prepare_centering(but_cont)

    but_cont2 = ttk.Frame(but_cont)
    but_cont2.grid(row=1, column=1, pady=(10, 0))

    style = ttk.Style()
    style.configure('UCS.TButton', font=tkg.button_regular_font_tuple())

    self.back_button = ttk.Button(but_cont2, text='Înapoi')
    self.back_button.config(style='UCS.TButton', command=self.back_click)
    self.back_button.grid(row=0, column=0, padx=5)

    self.create_button = ttk.Button(but_cont2, text='Creează')
    self.create_button.config(style='UCS.TButton', command=self.create_click)
    self.create_button.grid(row=0, column=1, padx=5)

  def back_click(self):
    self.controller.show_start_screen()

  def create_click(self):
    name = self.user_entry.get()
    if len(name) <= 0:
      self.error_label.config(text='Introdu numele utilizatorului.')
      self.clear_password_fields()
      return

    if ' ' in name:
      self.error_label.config(text='Numele nu poate conține spații.')
      self.clear_password_fields()
      return

    if len(name) < 4 or len(name) > 32:
      self.error_label.config(text='Numele trebuie să aibă\nîntre 4 și 32 de caractere.')
      self.clear_password_fields()
      return

    if name == userdb.DB_NAME:
      self.error_label.config(text='Ai ales un nume interesant, dar\neste deja rezervat. Îmi pare rău.')
      self.clear_password_fields()
      return

    pass1 = self.pass_entry1.get()
    pass2 = self.pass_entry2.get()
    if len(pass1) <= 0 or len(pass2) <= 0:
      self.error_label.config(text='Introdu parolele.')
      self.clear_password_fields()
      return

    if pass1 != pass2:
      self.error_label.config(text='Parolele nu corespund.')
      self.clear_password_fields()
      return

    if len(pass1) < 5 or len(pass1) > 64:
      self.error_label.config(text='Parola trebuie să aibă\n între 5 și 64 de caractere.')
      self.clear_password_fields()
      return

    self.add_to_database(name, pass1)

  def add_to_database(self, name, password):
    us = user.create_user(name, password)
    try:
      userdb.insert_user(us)
      accountdb.create_database(us)
      self.error_label.config(text='Utilizatorul a fost creat cu succes.')
    except userdb.UserExistsException:
      self.error_label.config(text='Utilizatorul există deja.')
    self.clear_password_fields()

  def clear_password_fields(self):
    self.pass_entry1.delete(0, tk.END)
    self.pass_entry2.delete(0, tk.END)
