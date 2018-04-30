from tkinter import ttk

import tkinter as tk

import platform

import accountchange
import accountdisplay
import exportdb
import importdb
import start
import usercreate
import userdelete
import usermenu

import userdb
import utils

class MainApp(tk.Tk):
  """ Model the main application. """

  def __init__(self, *args, **kwargs):
    """ Initialize the window and start the program. """
    tk.Tk.__init__(self, *args, **kwargs)
    self.geometry('450x550' if platform.system() == 'Windows' else '500x600')
    self.title('Administrator parole')
    self.resizable(width=False, height=False)

    if platform.system() != 'Windows':
      icon = tk.PhotoImage(file=utils.get_resource_path('images', 'icon.gif'))
      self.tk.call('wm', 'iconphoto', self._w, icon)
    else:
      self.iconbitmap(utils.get_resource_path('images', 'icon.ico'))

    self.frame = None
    self.show_start_screen()

  def clear_screen(self):
    """ Destroy the current frame. """
    if self.frame is not None:
      self.frame.destroy()

  def show_start_screen(self):
    """ Show the start screen. """
    self.clear_screen()
    self.frame = start.StartScreen(self)
    self.frame.pack(fill=tk.BOTH)

  def show_user_menu_screen(self, us):
    """ Show the user menu for a specified user. """
    self.clear_screen()
    self.frame = usermenu.UserMenuScreen(self, us)
    self.frame.pack(fill=tk.BOTH)

  def show_user_create_screen(self):
    """ Show the user-creation screen. """
    self.clear_screen()
    self.frame = usercreate.UserCreateScreen(self)
    self.frame.pack(fill=tk.BOTH)

  def show_user_delete_screen(self):
    """ Show the user-deletion screen. """
    self.clear_screen()
    self.frame = userdelete.UserDeleteScreen(self)
    self.frame.pack(fill=tk.BOTH)

  def show_account_display_screen(self, us):
    """ Show the account-display screen for a speciefied user. """
    self.clear_screen()
    self.frame = accountdisplay.AccountDisplayScreen(self, us)
    self.frame.pack(fill=tk.BOTH)

  def show_account_change_screen(self, us, acc):
    """ Show the data-changing screen for a user's account. """
    self.clear_screen()
    self.frame = accountchange.AccountChangeScreen(self, us, acc)
    self.frame.pack(fill=tk.BOTH)

  def show_export_screen(self, us):
    """ Show the database export screen for a specified user. """
    self.clear_screen()
    self.frame = exportdb.ExportDbScreen(self, us)
    self.frame.pack(fill=tk.BOTH)

  def show_import_screen(self, us):
    """ Show the database import screen for a specified user. """
    self.clear_screen()
    self.frame = importdb.ImportDbScreen(self, us)
    self.frame.pack(fill=tk.BOTH)


def main():
  """ Start the application. """
  try:
    userdb.create_database()
  except FileExistsError:
    pass
  app = MainApp()
  app.mainloop()


if __name__ == '__main__':
  main()

