import tkinter as tk

import utils

class HideButton(tk.Button):
  def __init__(self, parent, entry):
    tk.Button.__init__(self, parent)
    self.parent = parent
    self.entry = entry

    show_image_path = utils.get_resource_path('images', 'show.gif')
    self.show_image = tk.PhotoImage(file=show_image_path)

    hide_image_path = utils.get_resource_path('images', 'hide.gif')
    self.hide_image = tk.PhotoImage(file=hide_image_path)

    self.config(command=self.click)
    self.hide()

  def change_image(self, new_image):
    self.config(image=new_image)

  def show(self):
    self.entry.config(show='')
    self.change_image(self.show_image)

  def hide(self):
    self.entry.config(show='*')
    self.change_image(self.hide_image)

  def click(self):
    if self.entry.cget('show') == '*':
      self.show()
    else:
      self.hide()

