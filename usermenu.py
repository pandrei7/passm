from tkinter import ttk
from tkinter.ttk import *

import tkglobals as tkg
import tkinter as tk
import tkutils as tku

import passgenerator

class UserMenuScreen(ttk.Frame):
  def __init__(self, parent, us):
    ttk.Frame.__init__(self, parent)
    self.controller = parent
    self.us = us

    tku.prepare_centering(self)

    self.container = ttk.Frame(self)
    self.container.grid(row=1, column=1, sticky='nsew', padx=10, pady=20)

    self.place_main_gui()
    self.place_button_gui()

  def place_main_gui(self):
    cont = self.container

    self.title = ttk.Label(cont, text=self.us.name)
    self.title.config(font=tkg.title_font())
    self.title.grid(row=0, column=0, sticky='w', padx=15, pady=(10, 20))

  def place_button_gui(self):
    cont = self.container

    style = ttk.Style()
    style.configure('UMS.TButton', font=tkg.button_regular_font())

    self.acc_button = ttk.Button(cont, text='Conturi', width=25)
    self.acc_button.config(command=self.acc_click, style='UMS.TButton')
    self.acc_button.grid(row=1, column=0, padx=10, pady=7)

    self.pass_button = ttk.Button(cont, text='Generează o parolă', width=25)
    self.pass_button.config(command=self.pass_click, style='UMS.TButton')
    self.pass_button.grid(row=2, column=0, padx=10, pady=7)

    self.back_button = ttk.Button(cont, text='Înapoi', width=25)
    self.back_button.config(command=self.back_click, style='UMS.TButton')
    self.back_button.grid(row=3, column=0, padx=10, pady=7)

  def acc_click(self):
    self.controller.show_account_display_screen(self.us)

  def pass_click(self):
    son = tk.Toplevel(self)
    son.wm_title('Generator parolă')
    son.wm_resizable(width=False, height=False)
    gen = passgenerator.PassGeneratorFrame(son)
    gen.grid()

  def back_click(self):
    self.controller.show_start_screen()

