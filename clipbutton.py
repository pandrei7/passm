from tkinter.messagebox import showinfo
import tkinter as tk

import utils

class ClipButton(tk.Button):
  """ Model a button used to copy entry text to the clipboard. """

  def __init__(self, parent, entry, pop_title=None, pop_message=None):
    """ Initialize the object.

    The button is displayed with a special image. (images/clipboard.gif)

    :param parent: the parent of the button
    :param entry: the entry whose text is copied
    :param pop_title: the title of the pop-up window
    :param pop_message: the content of the pop-up message
    """

    tk.Button.__init__(self, parent)
    self.parent = parent
    self.entry = entry

    self.title = pop_title
    if self.title is None:
      self.title = 'Copiat!'

    self.message = pop_message
    if self.message is None:
      self.message = ('Am copiat textul.\n'
                      'Îl poți lipi doar dacă aplicația este deschisă.')

    image_path = utils.get_resource_path('images', 'clipboard.gif')
    self.image = tk.PhotoImage(file=image_path)

    self.config(image=self.image)
    self.config(command=self.click)

  def pop_up(self):
    """ Display the pop-up window. """
    showinfo(title=self.title, message=self.message, parent=self)

  def click(self):
    """ Copy the text to the system keyboard and display the pop-up. """
    r = tk.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(self.entry.get())
    r.update()
    r.destroy()

    self.pop_up()

