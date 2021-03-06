from tkinter import ttk

import tkglobals as tkg
import tkinter as tk
import tkutils as tku

import account
import accountdb
import user

class AccountDisplayScreen(ttk.Frame):
  """ Model the screen which displays a user's list of accounts. """

  def __init__(self, parent, us):
    """ Initialize the frame.
    
    :param parent: the controller of the frame
    :param us: the User who owns the accounts
    """
    ttk.Frame.__init__(self, parent)
    self.controller = parent
    self.us = us

    tku.prepare_centering(self)

    self.container = ttk.Frame(self)
    self.container.grid(row=1, column=1)

    self.place_main_gui()
    self.place_button_gui()

    self.load_accounts()

  def place_main_gui(self):
    """ Place the simple GUI objects in the frame. """
    cont = self.container

    self.title = ttk.Label(cont, text=self.us.name)
    self.title.config(font=tkg.title_font())
    self.title.grid(row=0, column=0, sticky='w', padx=(25, 0), pady=(30, 0))

    list_cont = ttk.Frame(cont)
    list_cont.grid(row=1, column=0, rowspan=4, pady=(20, 0))

    # The scrollbar needs to be packed before the listbox.
    self.scrollbar = tk.Scrollbar(list_cont, width=15)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    self.listbox = tk.Listbox(list_cont)
    self.listbox.config(font=tkg.regular_font(),
                        yscrollcommand=self.scrollbar.set)
    self.listbox.pack(side=tk.LEFT, fill=tk.Y)

    self.scrollbar.config(command=self.listbox.yview)

    self.listbox.bind('<Double-Button-1>', self.mod_click_decorator)

  def place_button_gui(self):
    """ Place the button-related GUI in the frame. """
    cont = self.container

    style = ttk.Style()
    style.configure('ADS.TButton', font=tkg.button_regular_font_tuple())
    style.configure('ADS_IMPORTANT.TButton',
                    font=tkg.button_bold_regular_font_tuple(),
                    foreground='red')

    self.add_button = ttk.Button(cont, text='Adaugă')
    self.add_button.config(style='ADS.TButton', command=self.add_click)
    self.add_button.grid(row=1, column=1, sticky='ew', padx=(20, 0), pady=(20, 0))

    self.mod_button = ttk.Button(cont, text='Modifică')
    self.mod_button.config(style='ADS.TButton', command=self.mod_click)
    self.mod_button.grid(row=2, column=1, sticky='ew', padx=(20, 0))

    self.delete_button = ttk.Button(cont, text='Șterge')
    self.delete_button.config(style='ADS_IMPORTANT.TButton',
                              command=self.delete_click)
    self.delete_button.grid(row=3, column=1, sticky='ew', padx=(20, 0))

    self.back_button = ttk.Button(cont, text='Înapoi')
    self.back_button.config(style='ADS.TButton', command=self.back_click)
    self.back_button.grid(row=4, column=1, sticky='ew', padx=(20, 0))

    self.search_entry = ttk.Entry(cont)
    self.search_entry.config(font=tkg.regular_font())
    self.search_entry.grid(row=5, column=0, sticky='ew', pady=20)

    self.search_button = ttk.Button(cont, text='Caută')
    self.search_button.config(style='ADS.TButton', command=self.search_click)
    self.search_button.grid(row=5, column=1, sticky='ew', padx=(20, 0))

  def load_accounts(self, query=''):
    """ Load all accounts that meet a criteria on the screen. 
    
    Only accounts whose names contain the query as a substring
    are displayed on the screen.
    """

    # Create user's database if it does not exist (possible bug).
    # This might be needed if the user's database file is deleted
    # outside the app.
    accountdb.create_database(self.us)

    self.listbox.delete(0, tk.END)
    accounts = accountdb.get_accounts_by_name(self.us, query)

    for acc in accounts:
      a = account.unpack(acc)
      self.listbox.insert(tk.END, a.name)

  def add_click(self):
    """ Go to the add-new-account screen. """
    self.controller.show_account_change_screen(self.us, None)

  def mod_click_decorator(self, aux):
    self.mod_click()

  def mod_click(self):
    """ Modify the account selected by the user. """
    selection = self.listbox.curselection()
    if len(selection) <= 0:
      return

    acc_name = self.listbox.get(selection[0])
    acc = accountdb.get_accounts_by_name_exact(self.us, acc_name)[0]
    acc = account.unpack(acc)
    self.controller.show_account_change_screen(self.us, acc)

  def delete_click(self):
    """ Delete the account selected by the user. """
    selection = self.listbox.curselection()
    if len(selection) <= 0:
      return

    acc_name = self.listbox.get(selection[0])
    acc = accountdb.get_accounts_by_name_exact(self.us, acc_name)[0]
    acc = account.unpack(acc)
    accountdb.delete_account(self.us, acc)
    self.load_accounts()

  def back_click(self):
    """ Go to the previous screen. """
    self.controller.show_user_menu_screen(self.us)

  def search_click(self):
    """ Load the accounts which meet the search-criteria. """
    query = self.search_entry.get()
    self.load_accounts(query)

