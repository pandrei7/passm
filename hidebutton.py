import tkinter as tk

import utils

class HideButton(tk.Button):
  """ Model a button used to hide and show the text of an entry. """

  def __init__(self, parent, entry):
    """ Initialize the object.

    The button is displayed with two special images that are switched
    automatically. (images/show.gif and images/hide.gif)

    :param parent: the parent of the button
    :param entry: the entry which the button controls
    """

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
    """ Change the displayed image to the new_image. """
    self.config(image=new_image)

  def show(self):
    """ Show the entry text. """
    self.entry.config(show='')
    self.change_image(self.show_image)

  def hide(self):
    """ Hide the entry text. """
    self.entry.config(show='*')
    self.change_image(self.hide_image)

  def click(self):
    """ Toggle text visibility. """
    if self.entry.cget('show') == '*':
      self.show()
    else:
      self.hide()

