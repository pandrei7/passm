from tkinter import ttk
from tkinter.ttk import *

import tkglobals as tkg
import tkinter as tk

import accountdb
import user
import userdb

class UserDeleteScreen(ttk.Frame):
  def __init__(self, parent):
    ttk.Frame.__init__(self, parent)
    self.controller = parent

    style = ttk.Style()

    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(2, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(2, weight=1)

    container = ttk.Frame(self)
    container.grid(row=1, column=1, sticky='nsew', pady=(30, 0))

    self.title = ttk.Label(container, text='Șterge un cont')
    self.title.config(font=tkg.title_font())
    self.title.grid(row=0, column=0, sticky='w')

    self.label1 = ttk.Label(container, text='Utilizator')
    self.label1.config(font=tkg.regular_font())
    self.label1.grid(row=1, column=0, sticky='w', pady=(30, 0))

    self.user_entry = ttk.Entry(container)
    self.user_entry.config(font=tkg.regular_font())
    self.user_entry.grid(row=2, column=0, sticky='ew', pady=(5, 0))

    self.label2 = ttk.Label(container, text='Parolă')
    self.label2.config(font=tkg.regular_font())
    self.label2.grid(row=3, column=0, sticky='w', pady=(10, 0))

    self.pass_entry1 = ttk.Entry(container, show='*')
    self.pass_entry1.config(font=tkg.regular_font())
    self.pass_entry1.grid(row=4, column=0, sticky='ew', pady=(5, 0))

    self.label3 = ttk.Label(container, text='Parolă (din nou)')
    self.label3.config(font=tkg.regular_font())
    self.label3.grid(row=5, column=0, sticky='w', pady=(10, 0))

    self.pass_entry2 = ttk.Entry(container, show='*')
    self.pass_entry2.config(font=tkg.regular_font())
    self.pass_entry2.grid(row=6, column=0, sticky='ew', pady=(5, 0))

    self.error_label = tk.Label(container, text='')
    self.error_label.config(font=tkg.small_regular_font(), fg='red')
    self.error_label.grid(row=7, column=0, pady=(10, 0))

    but_container = ttk.Frame(container)
    but_container.grid(row=8, column=0)
    but_container.grid_rowconfigure(0, weight=1)
    but_container.grid_rowconfigure(2, weight=1)
    but_container.grid_columnconfigure(0, weight=1)
    but_container.grid_columnconfigure(2, weight=1)

    but_container2 = ttk.Frame(but_container)
    but_container2.grid(row=1, column=1, pady=(10, 0))

    style.configure('UDS.TButton', font=tkg.button_regular_font_tuple())
    style.configure('UDS_IMPORTANT.TButton',
                    font=tkg.button_bold_regular_font_tuple(),
                    foreground='red')

    self.back_button = ttk.Button(but_container2, text='Înapoi')
    self.back_button.config(style='UDS.TButton', command=self.back_click)
    self.back_button.grid(row=0, column=0, sticky='ns', padx=5)

    self.delete_button = ttk.Button(but_container2, text='Șterge')
    self.delete_button.config(style='UDS_IMPORTANT.TButton',
                              command=self.delete_click)
    self.delete_button.grid(row=0, column=1, sticky='ns', padx=5)

  def back_click(self):
    self.controller.show_start_screen()

  def delete_click(self):
    name = self.user_entry.get()
    if len(name) <= 0:
      self.error_label.config(text='Introdu numele utilizatorului.')
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

    self.remove_from_database(name, pass1)
    self.clear_password_fields()

  def remove_from_database(self, name, password):
    us = userdb.get_users_by_name_exact(name)
    if len(us) <= 0:
      self.error_label.config(text='Nu am găsit niciun utilizator cu acest nume.')
      return
    if len(us) > 1:
      self.error_label.config(text='Chestia asta nu trebuia să se întâmple...')
      return

    try:
      if userdb.password_check(name, password):
        us = user.unpack(us[0])
        userdb.delete_user(us)
        accountdb.delete_database(us)
        self.error_label.config(text='Contul ' + name + '\na fost eliminat cu succes.')
      else:
        self.error_label.config(text='Parolă greșită.')
    except userdb.UserNotFoundException:
      self.error_label.config(text="Are you trying to cheat?\nYou're so funny, " + name + ".")

  def clear_password_fields(self):
    self.pass_entry1.delete(0, tk.END)
    self.pass_entry2.delete(0, tk.END)
