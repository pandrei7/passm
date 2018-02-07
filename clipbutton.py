from tkinter.messagebox import showinfo
import tkinter as tk

class ClipButton(tk.Button):
    def __init__(self, parent, entry, pop_title=None, pop_message=None):
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

        self.image = tk.PhotoImage(file='images/clipboard.gif')
        self.config(image=self.image)
        self.config(command=self.click)

    def pop_up(self):
        showinfo(title=self.title, message=self.message, parent=self)

    def click(self):
        r = tk.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(self.entry.get())
        r.update()
        r.destroy()

        self.pop_up()

