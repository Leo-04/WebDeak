from tkinter import *


class TkMenu(Frame):
    def __init__(self, master, *commands):
        Frame.__init__(self, master, bd=2, relief="raised")

        for cmd in commands:
            if cmd is None:
                self.add_seperator()
            else:
                self.add_command(*cmd)

    def add_seperator(self):
        Label(self, padx=20).pack(side=LEFT)

    def add_command(self, name, hotkey=None, callback=None):
        button = Button(self, text=name, command=callback, padx=10, pady=2, relief="flat")
        button.pack(side=LEFT)
        button.bind("<ButtonPress-1>", lambda e: button.config(relief="sunken"))
        button.bind("<ButtonRelease-1>", lambda e: button.config(relief="flat"))

        self.winfo_toplevel().bind_all(hotkey, lambda e: callback())

