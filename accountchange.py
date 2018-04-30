from tkinter import ttk

import tkglobals as tkg
import tkinter as tk
import tkutils as tku

import platform

import clipbutton
import hidebutton
import passgenerator

import account
import accountdb
import secrets
import user
import utils

class AccountChangeScreen(ttk.Frame):
  """ Model the screen where the user can change account data. 
  
  This screen can be used both to modify an existing account
  and to create a new one.
  """

  def __init__(self, parent, us, acc=None):
    """ Initialize the frame. 
    
    :param parent: the controller of the frame
    :param us: the User who owns the Account
    :param acc: the Account; if None, assumes a new account
    """

    ttk.Frame.__init__(self, parent)
    self.controller = parent
    self.us = us
    self.acc = acc

    tku.prepare_centering(self)

    self.container = ttk.Frame(self)
    self.container.grid(row=1, column=1, padx=20)

    self.place_main_gui()
    self.place_button_gui()

    self.is_new_account = (acc is None)
    self.load_account_data()

  def place_main_gui(self):
    """ Place the simple GUI objects in the frame. """
    cont = self.container

    self.title = ttk.Label(cont, text='Detaliile contului')
    self.title.config(font=tkg.title_font())
    self.title.grid(row=0, column=0, sticky='w', pady=(30, 0))

    self.label1 = ttk.Label(cont, text='Nume cont')
    self.label1.config(font=tkg.regular_font())
    self.label1.grid(row=1, column=0, sticky='w', padx=5, pady=(30, 0))

    self.name_entry = ttk.Entry(cont)
    self.name_entry.config(font=tkg.regular_font())
    self.name_entry.grid(row=2, column=0, sticky='ew', pady=(5, 0))
    if platform.system() != 'Windows':
      self.name_entry.grid(padx=(0, 10))

    self.label2 = ttk.Label(cont, text='Email')
    self.label2.config(font=tkg.regular_font())
    self.label2.grid(row=3, column=0, sticky='w', padx=5, pady=(10, 0))

    self.email_entry = ttk.Entry(cont)
    self.email_entry.config(font=tkg.regular_font())
    self.email_entry.grid(row=4, column=0, sticky='ew', pady=(5, 0))
    if platform.system() != 'Windows':
      self.email_entry.grid(padx=(0, 10))

    self.label3 = ttk.Label(cont, text='Nume de utilizator')
    self.label3.config(font=tkg.regular_font())
    self.label3.grid(row=5, column=0, sticky='w', padx=5, pady=(10, 0))

    self.user_entry = ttk.Entry(cont)
    self.user_entry.config(font=tkg.regular_font())
    self.user_entry.grid(row=6, column=0, sticky='ew', pady=(5, 0))
    if platform.system() != 'Windows':
      self.user_entry.grid(padx=(0, 10))

    self.label4 = ttk.Label(cont, text='Parolă')
    self.label4.config(font=tkg.regular_font())
    self.label4.grid(row=7, column=0, sticky='w', padx=5, pady=(10, 0))

    pass_cont = ttk.Frame(cont)
    pass_cont.grid(row=8, column=0, sticky='ew')

    self.pass_entry = ttk.Entry(pass_cont, show='*', width=27)
    self.pass_entry.config(font=tkg.regular_font())
    self.pass_entry.grid(row=0, column=0, padx=(0, 10), pady=(5, 0))

    self.hide_button = hidebutton.HideButton(pass_cont, self.pass_entry)
    self.hide_button.grid(row=0, column=1, padx=(0, 10), pady=(5, 0))

    self.clip_button = clipbutton.ClipButton(pass_cont, self.pass_entry)
    self.clip_button.grid(row=0, column=2, pady=(5, 0))

    self.error_label = tk.Label(cont, text='')
    self.error_label.config(font=tkg.small_regular_font(), fg='red')
    self.error_label.grid(row=9, column=0, pady=(10, 10))

  def place_button_gui(self):
    """ Place the button-related GUI in the frame. """
    cont = self.container

    # This container is used for centering.
    but_cont = ttk.Frame(cont)
    but_cont.grid(row=10, column=0, sticky='ew')
    tku.prepare_centering(but_cont)

    # This container actually holds the buttons.
    but_cont2 = ttk.Frame(but_cont)
    but_cont2.grid(row=1, column=1)

    style = ttk.Style()
    style.configure('ACS.TButton', font=tkg.button_regular_font_tuple())

    self.back_button = ttk.Button(but_cont2, text='Înapoi')
    self.back_button.config(style='ACS.TButton', command=self.back_click)
    self.back_button.grid(row=0, column=0, sticky='ns', padx=5)

    self.save_button = ttk.Button(but_cont2, text='Salvează')
    self.save_button.config(style='ACS.TButton', command=self.save_click)
    self.save_button.grid(row=0, column=1, sticky='ns', padx=5)

    self.pass_button = ttk.Button(but_cont2, text='Generează parolă')
    self.pass_button.config(style='ACS.TButton', command=self.pass_click)
    self.pass_button.grid(row=0, column=2, sticky='ns', padx=5)

  def back_click(self):
    """ Go to the previous screen. """
    self.controller.show_account_display_screen(self.us)

  def save_click(self):
    """ Save the modified account data. """
    acc_name = self.name_entry.get()
    email = self.email_entry.get()
    username = self.user_entry.get()
    password = self.pass_entry.get()

    if not acc_name:
      self.error_label.config(text='Introdu numele contului.')
      return

    if self.is_new_account and accountdb.account_exists(self.us, acc_name):
      self.error_label.config(text='Un cont cu acest nume există deja.')
      return

    # Tell the user what's happening.
    self.error_label.config(text='Se salvează...')
    self.error_label.update()

    acc = account.create_account(acc_name, email, username, password, self.us)
    accountdb.change_account(self.us, acc)

    self.error_label.config(text='Detaliile contului au fost salvate.')

    self.acc = acc
    self.is_new_account = False
    self.load_account_data()

  def pass_click(self):
    """ Open the password generator window. """
    son = tk.Toplevel(self)
    son.wm_title('Generator parolă')
    son.wm_resizable(width=False, height=False)

    if platform.system() != 'Windows':
      icon = tk.PhotoImage(file=utils.get_resource_path('images', 'icon.gif'))
      son.tk.call('wm', 'iconphoto', son._w, icon)
    else:
      son.wm_iconbitmap(utils.get_resource_path('images', 'icon.ico'))

    pop_up_icon_path = utils.get_resource_path('images', 'icon.gif')
    pop_up_icon = tk.PhotoImage(file=pop_up_icon_path)
    son.tk.call('wm', 'iconphoto', son._w, pop_up_icon)

    gen = passgenerator.PassGeneratorFrame(son)
    gen.grid()

  def load_account_data(self):
    """ Display the data of the account on the screen. """
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

