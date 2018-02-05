import tkinter as tk

class HideButton(tk.Button):
    def __init__(self, parent, entry):
        tk.Button.__init__(self, parent)
        self.parent = parent
        self.entry = entry

        self.show_image = tk.PhotoImage(file='images/show.gif')
        self.hide_image = tk.PhotoImage(file='images/hide.gif')

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
