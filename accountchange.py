from tkinter import ttk
from tkinter.ttk import *

import tkglobals as tkg
import tkinter as tk

import account
import accountdb
import clipbutton
import hidebutton
import passgenerator
import secrets
import user

class AccountChangeScreen(ttk.Frame):
  def __init__(self, parent, us, acc=None):
    ttk.Frame.__init__(self, parent)
    self.controller = parent
    self.us = us
    self.acc = acc

    style = ttk.Style()

    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(2, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(2, weight=1)

    container = ttk.Frame(self)
    container.grid(row=1, column=1, padx=20)

    self.title = ttk.Label(container, text='Detaliile contului')
    self.title.config(font=tkg.title_font())
    self.title.grid(row=0, column=0, sticky='w', pady=(30, 0))

    self.label1 = ttk.Label(container, text='Nume cont')
    self.label1.config(font=tkg.regular_font())
    self.label1.grid(row=1, column=0, sticky='w', padx=5, pady=(30, 0))

    self.name_entry = ttk.Entry(container)
    self.name_entry.config(font=tkg.regular_font())
    self.name_entry.grid(row=2, column=0, sticky='ew', pady=(5, 0))

    self.label2 = ttk.Label(container, text='Email')
    self.label2.config(font=tkg.regular_font())
    self.label2.grid(row=3, column=0, sticky='w', padx=5, pady=(10, 0))

    self.email_entry = ttk.Entry(container)
    self.email_entry.config(font=tkg.regular_font())
    self.email_entry.grid(row=4, column=0, sticky='ew', pady=(5, 0))

    self.label3 = ttk.Label(container, text='Nume de utilizator')
    self.label3.config(font=tkg.regular_font())
    self.label3.grid(row=5, column=0, sticky='w', padx=5, pady=(10, 0))

    self.user_entry = ttk.Entry(container)
    self.user_entry.config(font=tkg.regular_font())
    self.user_entry.grid(row=6, column=0, sticky='ew', pady=(5, 0))

    self.label4 = ttk.Label(container, text='Parolă')
    self.label4.config(font=tkg.regular_font())
    self.label4.grid(row=7, column=0, sticky='w', padx=5, pady=(10, 0))

    pass_container = ttk.Frame(container)
    pass_container.grid(row=8, column=0, sticky='ew')

    self.pass_entry = ttk.Entry(pass_container, show='*', width=27)
    self.pass_entry.config(font=tkg.regular_font())
    self.pass_entry.grid(row=0, column=0, padx=(0, 10), pady=(5, 0))

    self.hide_button = hidebutton.HideButton(pass_container, self.pass_entry)
    self.hide_button.grid(row=0, column=1, padx=(0, 10), pady=(5, 0))

    self.clip_button = clipbutton.ClipButton(pass_container, self.pass_entry)
    self.clip_button.grid(row=0, column=2, pady=(5, 0))

    self.error_label = tk.Label(container, text='')
    self.error_label.config(font=tkg.small_regular_font(), fg='red')
    self.error_label.grid(row=9, column=0, pady=(10, 10))

    but_container = ttk.Frame(container)
    but_container.grid(row=10, column=0, sticky='ew')
    but_container.grid_rowconfigure(0, weight=1)
    but_container.grid_rowconfigure(2, weight=1)
    but_container.grid_columnconfigure(0, weight=1)
    but_container.grid_columnconfigure(2, weight=1)

    but_container2 = ttk.Frame(but_container)
    but_container2.grid(row=1, column=1)

    style.configure('ACS.TButton', font=tkg.button_regular_font())

    self.back_button = ttk.Button(but_container2, text='Înapoi')
    self.back_button.config(style='ACS.TButton', command=self.back_click)
    self.back_button.grid(row=0, column=0, sticky='ns', padx=5)

    self.save_button = ttk.Button(but_container2, text='Salvează')
    self.save_button.config(style='ACS.TButton', command=self.save_click)
    self.save_button.grid(row=0, column=1, sticky='ns', padx=5)

    self.pass_button = ttk.Button(but_container2, text='Generează parolă')
    self.pass_button.config(style='ACS.TButton', command=self.pass_click)
    self.pass_button.grid(row=0, column=2, sticky='ns', padx=5)

    self.load_account_data()

  def back_click(self):
    self.controller.show_account_display_screen(self.us)

  def save_click(self):
    acc_name = self.name_entry.get()
    if len(acc_name) <= 0:
      self.error_label.config(text='Introdu numele contului.')
      return

    email = self.email_entry.get()
    username = self.user_entry.get()
    password = self.pass_entry.get()

    self.error_label.config(text='Se salvează...')
    self.error_label.update()

    acc = account.create_account(acc_name, email, username, password, self.us)
    accountdb.change_account(self.us, acc)

    self.error_label.config(text='Detaliile contului au fost salvate.')

    self.acc = acc
    self.load_account_data()

  def pass_click(self):
    son = tk.Toplevel(self)
    son.wm_title('Generator parolă')
    son.wm_resizable(width=False, height=False)
    gen = passgenerator.PassGeneratorFrame(son)
    gen.grid()

  def load_account_data(self):
    if self.acc is None:
      return

    self.name_entry.delete(0, tk.END)
    self.name_entry.insert(0, self.acc.name)
    self.name_entry.config(state='disabled')

    self.email_entry.delete(0, tk.END)
    self.email_entry.insert(0, self.acc.email)

    self.user_entry.delete(0, tk.END)
    self.user_entry.insert(0, self.acc.username)

    key = secrets.decrypt_field(self.us.crypt_key)
    self.pass_entry.delete(0, tk.END)
    self.pass_entry.insert(0, secrets.decrypt_data(key, self.acc.password))
