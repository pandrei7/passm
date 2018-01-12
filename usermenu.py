from tkinter import ttk
from tkinter.ttk import *

import passgenerator
import tkglobals as tkg
import tkinter as tk

class UserMenuScreen(tk.Frame):
  def __init__(self, parent, us):
    tk.Frame.__init__(self, parent)
    self.controller = parent

    style = ttk.Style()

    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(2, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(2, weight=1)

    container = ttk.Frame(self)
    container.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

    self.title = ttk.Label(container, text=us.name)
    self.title.config(font=tkg.title_font())
    self.title.grid(row=0, column=0, sticky='w', padx=15, pady=(10, 20))

    style.configure('UMS.TButton', font=tkg.regular_font())

    self.acc_button = ttk.Button(container, text='Conturi', width=25)
    self.acc_button.config(command=self.acc_click, style='UMS.TButton')
    self.acc_button.grid(row=1, column=0, padx=10, pady=7)

    self.pass_button = ttk.Button(container, text='Generează o parolă', width=25)
    self.pass_button.config(command=self.pass_click, style='UMS.TButton')
    self.pass_button.grid(row=2, column=0, padx=10, pady=7)

    self.back_button = ttk.Button(container, text='Înapoi', width=25)
    self.back_button.config(command=self.back_click, style='UMS.TButton')
    self.back_button.grid(row=3, column=0, padx=10, pady=7)

  def acc_click(self):
    pass

  def pass_click(self):
    son = tk.Toplevel(self)
    son.wm_title('Generator parolă')
    gen = passgenerator.PassGeneratorFrame(son)
    gen.grid()

  def back_click(self):
    self.controller.show_start_screen()
