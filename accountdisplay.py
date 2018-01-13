from tkinter import ttk
from tkinter.ttk import *

import tkglobals as tkg
import tkinter as tk

import account
import accountdb
import user

class AccountDisplayScreen(ttk.Frame):
  def __init__(self, parent, us):
    ttk.Frame.__init__(self, parent)
    self.controller = parent
    self.us = us

    style = ttk.Style()

    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(2, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(2, weight=1)

    container = ttk.Frame(self)
    container.grid(row=1, column=1)

    self.title = ttk.Label(container, text=us.name)
    self.title.config(font=tkg.title_font())
    self.title.grid(row=0, column=0, sticky='w', padx=(25, 0), pady=(30, 0))

    list_container = ttk.Frame(container)
    list_container.grid(row=1, column=0, rowspan=4, pady=(20, 0))

    self.scrollbar = tk.Scrollbar(list_container, width=15)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    self.listbox = tk.Listbox(list_container)
    self.listbox.config(font=tkg.regular_font(),
                        yscrollcommand=self.scrollbar.set)
    self.listbox.pack(side=tk.LEFT, fill=tk.Y)

    self.listbox.bind('<Double-Button-1>', self.mod_click_decorator)
    self.load_accounts()

    style.configure('ADS.TButton', font=tkg.button_regular_font_tuple())
    style.configure('ADS_IMPORTANT.TButton',
                    font=tkg.button_bold_regular_font_tuple(),
                    foreground='red')

    self.add_button = ttk.Button(container, text='Adaugă')
    self.add_button.config(style='ADS.TButton', command=self.add_click)
    self.add_button.grid(row=1, column=1, sticky='ew', padx=(20, 0), pady=(20, 0))

    self.mod_button = ttk.Button(container, text='Modifică')
    self.mod_button.config(style='ADS.TButton', command=self.mod_click)
    self.mod_button.grid(row=2, column=1, sticky='ew', padx=(20, 0))

    self.delete_button = ttk.Button(container, text='Șterge')
    self.delete_button.config(style='ADS_IMPORTANT.TButton',
                              command=self.delete_click)
    self.delete_button.grid(row=3, column=1, sticky='ew', padx=(20, 0))

    self.back_button = ttk.Button(container, text='Înapoi')
    self.back_button.config(style='ADS.TButton', command=self.back_click)
    self.back_button.grid(row=4, column=1, sticky='ew', padx=(20, 0))

    self.search_entry = ttk.Entry(container)
    self.search_entry.config(font=tkg.regular_font())
    self.search_entry.grid(row=5, column=0, sticky='ew', pady=20)

    self.search_button = ttk.Button(container, text='Caută')
    self.search_button.config(style='ADS.TButton', command=self.search_click)
    self.search_button.grid(row=5, column=1, sticky='ew', padx=(20, 0))

  def load_accounts(self, query=''):
    self.listbox.delete(0, tk.END)
    accounts = accountdb.get_accounts_by_name(self.us, query)

    for acc in accounts:
      a = account.unpack(acc)
      self.listbox.insert(tk.END, a.name)

  def add_click(self):
    self.controller.show_account_change_screen(self.us, None)

  def mod_click_decorator(self, aux):
    self.mod_click()

  def mod_click(self):
    pass

  def delete_click(self):
    pass

  def back_click(self):
    self.controller.show_user_menu_screen(self.us)

  def search_click(self):
    query = self.search_entry.get()
    self.load_accounts(query)
