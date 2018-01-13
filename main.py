from tkinter import ttk
from tkinter.ttk import *

import tkglobals as tkg
import tkinter as tk

import usercreate
import userdelete
import usermenu

import user
import userdb

class StartScreen(ttk.Frame):
  def __init__(self, parent):
    ttk.Frame.__init__(self, parent)
    self.controller = parent

    style = ttk.Style()

    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(2, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(2, weight=1)

    container = ttk.Frame(self)
    container.grid(row=1, column=1, sticky='nsew', padx=10)
    container.grid_rowconfigure(0, weight=1)
    container.grid_rowconfigure(2, weight=1)
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(2, weight=1)

    container_top = ttk.Frame(container)
    container_top.grid(row=0, column=0, pady=(30, 0))

    self.image = tk.PhotoImage(file='images/big.gif')
    self.image_label = ttk.Label(container_top, image=self.image)
    self.image_label.grid(row=0, column=0, sticky='w')

    self.title = ttk.Label(container_top, text='Manager parolă')
    self.title.config(font=tkg.hyper_title_font())
    self.title.grid(row=0, column=1, sticky='e', padx=10, pady=10)

    container_bot = ttk.Frame(container)
    container_bot.grid(row=1, column=0, pady=(40, 0))
    container_bot.grid_rowconfigure(0, weight=1)
    container_bot.grid_rowconfigure(2, weight=1)
    container_bot.grid_columnconfigure(0, weight=1)
    container_bot.grid_columnconfigure(2, weight=1)

    container_bot2 = ttk.Frame(container_bot)
    container_bot2.grid(row=1, column=1)

    self.label1 = ttk.Label(container_bot2, text='Utilizator')
    self.label1.config(font=tkg.regular_font())
    self.label1.grid(row=0, column=0, sticky='w')

    self.user_entry = ttk.Entry(container_bot2)
    self.user_entry.config(font=tkg.regular_font())
    self.user_entry.grid(row=1, column=0, sticky='ew')

    self.label2 = ttk.Label(container_bot2, text='Parolă')
    self.label2.config(font=tkg.regular_font())
    self.label2.grid(row=2, column=0, sticky='w', pady=(10, 0))

    self.pass_entry = ttk.Entry(container_bot2, show='*')
    self.pass_entry.config(font=tkg.regular_font())
    self.pass_entry.grid(row=3, column=0, sticky='ew')

    self.error_label = tk.Label(container_bot2, text='')
    self.error_label.config(font=tkg.small_regular_font(), fg='red')
    self.error_label.grid(row=4, column=0, sticky='ew', pady=(5, 0))

    style.configure('SS.TButton', font=tkg.button_regular_font())

    self.enter_button = ttk.Button(container_bot2, text='Intră')
    self.enter_button.config(style='SS.TButton', command=self.enter_click)
    self.enter_button.grid(row=5, column=0, sticky='ew', pady=(10, 5))

    self.new_button = ttk.Button(container_bot2, text='Utilizator nou')
    self.new_button.config(style='SS.TButton', command=self.new_click)
    self.new_button.grid(row=6, column=0, sticky='ew', pady=5)

    self.delete_button = ttk.Button(container_bot2, text='Șterge-mi contul')
    self.delete_button.config(style='SS.TButton', command=self.delete_click)
    self.delete_button.grid(row=7, column=0, sticky='ew', pady=(5, 10))


  def enter_click(self):
    name = self.user_entry.get()
    if len(name) <= 0:
      self.error_label.config(text='Introdu numele utilizatorului.')
      return

    password = self.pass_entry.get()
    if len(password) <= 0:
      self.error_label.config(text='Introdu parola.')
      return

    try:
      if userdb.password_check(name, password):
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
    self.controller.show_user_create_screen()

  def delete_click(self):
    self.controller.show_user_delete_screen()

  def clear_password_field(self):
    self.pass_entry.delete(0, tk.END)


class MainApp(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)
    self.geometry('500x600')
    self.title('Manager parolă')
    self.resizable(width=False, height=False)

    self.frame = None
    self.show_start_screen()

  def clear_screen(self):
    if self.frame is not None:
      self.frame.destroy()

  def show_start_screen(self):
    self.clear_screen()
    self.frame = StartScreen(self)
    self.frame.pack(fill=tk.BOTH)

  def show_user_menu_screen(self, us):
    self.clear_screen()
    self.frame = usermenu.UserMenuScreen(self, us)
    self.frame.pack(fill=tk.BOTH)

  def show_user_create_screen(self):
    self.clear_screen()
    self.frame = usercreate.UserCreateScreen(self)
    self.frame.pack(fill=tk.BOTH)

  def show_user_delete_screen(self):
    self.clear_screen()
    self.frame = userdelete.UserDeleteScreen(self)
    self.frame.pack(fill=tk.BOTH)


def main():
  app = MainApp()
  app.mainloop()


if __name__ == '__main__':
  main()
