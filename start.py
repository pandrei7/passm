from tkinter import ttk

import tkglobals as tkg
import tkinter as tk
import tkutils as tku

import user
import userdb
import utils

class StartScreen(ttk.Frame):
  """ Model the start screen. """

  def __init__(self, parent):
    """ Initialize the frame.

    :param parent: the controller of the frame.
    """

    ttk.Frame.__init__(self, parent)
    self.controller = parent

    tku.prepare_centering(self)

    self.container = ttk.Frame(self)
    self.container.grid(row=1, column=1, sticky='nsew', padx=10)
    tku.prepare_centering(self.container)

    self.place_main_gui()
    self.place_entry_gui()
    self.place_button_gui()

  def place_main_gui(self):
    """ Place the simple GUI objects in the frame. """
    cont = self.container

    top_cont = ttk.Frame(cont)
    top_cont.grid(row=0, column=0, pady=(30, 0))

    image_path = utils.get_resource_path('images', 'big.gif')
    self.image = tk.PhotoImage(file=image_path)
    self.image_label = ttk.Label(top_cont, image=self.image)
    self.image_label.grid(row=0, column=0, sticky='w')

    self.title = ttk.Label(top_cont, text='Administrator\nparole\n-Melcușor Pass-')
    self.title.config(font=tkg.hyper_title_font(), justify=tk.CENTER)
    self.title.grid(row=0, column=1, sticky='e', padx=10, pady=10)

  def place_entry_gui(self):
    """ Place the entry-related GUI in the frame. """
    cont = self.container

    bot_cont = ttk.Frame(cont)
    bot_cont.grid(row=1, column=0, pady=(40, 0))
    tku.prepare_centering(bot_cont)

    self.bot_cont2 = ttk.Frame(bot_cont)
    self.bot_cont2.grid(row=1, column=1)

    self.label1 = ttk.Label(self.bot_cont2, text='Utilizator')
    self.label1.config(font=tkg.regular_font())
    self.label1.grid(row=0, column=0, sticky='w')

    self.user_entry = ttk.Entry(self.bot_cont2)
    self.user_entry.config(font=tkg.regular_font())
    self.user_entry.grid(row=1, column=0, sticky='ew')

    self.label2 = ttk.Label(self.bot_cont2, text='Parolă')
    self.label2.config(font=tkg.regular_font())
    self.label2.grid(row=2, column=0, sticky='w', pady=(10, 0))

    self.pass_entry = ttk.Entry(self.bot_cont2, show='*')
    self.pass_entry.config(font=tkg.regular_font())
    self.pass_entry.grid(row=3, column=0, sticky='ew')

    self.error_label = tk.Label(self.bot_cont2, text='')
    self.error_label.config(font=tkg.small_regular_font(), fg='red')
    self.error_label.grid(row=4, column=0, sticky='ew', pady=(5, 0))

  def place_button_gui(self):
    """ Place the button-related GUI in the frame. """
    style = ttk.Style()
    style.configure('SS.TButton', font=tkg.button_regular_font_tuple())

    self.enter_button = ttk.Button(self.bot_cont2, text='Intră')
    self.enter_button.config(style='SS.TButton', command=self.enter_click)
    self.enter_button.grid(row=5, column=0, sticky='ew', pady=(10, 5))

    self.new_button = ttk.Button(self.bot_cont2, text='Utilizator nou')
    self.new_button.config(style='SS.TButton', command=self.new_click)
    self.new_button.grid(row=6, column=0, sticky='ew', pady=5)

    self.delete_button = ttk.Button(self.bot_cont2, text='Șterge-mi contul')
    self.delete_button.config(style='SS.TButton', command=self.delete_click)
    self.delete_button.grid(row=7, column=0, sticky='ew', pady=(5, 10))

  def enter_click(self):
    """ Log in the user. """
    name = self.user_entry.get()
    if not name:
      self.error_label.config(text='Introdu numele utilizatorului.')
      return

    password = self.pass_entry.get()
    if not password:
      self.error_label.config(text='Introdu parola.')
      return

    # Tell the user what's happening.
    self.error_label.config(text='Verific parola...')
    self.error_label.update()

    try:
      if userdb.check_password(name, password):
        self.error_label.config(text='Intru în cont...')
        self.error_label.update()
        us = userdb.get_users_by_name(name)[0]
        us = user.unpack(us)
        self.controller.show_user_menu_screen(us)
      else:
        self.error_label.config(text='Parolă greșită.')
        self.clear_password_field()
    except userdb.UserNotFoundException:
      self.error_label.config(text='Nu am găsit acest utilizator.')
      return

  def new_click(self):
    """ Go to the user-creation screen. """
    self.controller.show_user_create_screen()

  def delete_click(self):
    """ Go to the user-deletion screen. """
    self.controller.show_user_delete_screen()

  def clear_password_field(self):
    """ Empty the password field. """
    self.pass_entry.delete(0, tk.END)

