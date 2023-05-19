import json
from tkinter import Entry, Label
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import askyesnocancel, showerror, askyesno
from tkinter.simpledialog import askstring

from UI.board import Board
from UI.listbook import ListBook
from UI.tkmenu import TkMenu
from UI.window import Window


class App:
    def __init__(self, style_path):
        self.win = Window("WebSD", self.close)
        
        try:
            self.win.option_readfile(style_path)
        except:
            pass

        self.panels = ListBook()
        self.menu = TkMenu(self.win,
            ("New", "<Control-n>", self.new),
            ("Open", "<Control-o>", self.open),
            ("Save", "<Control-s>", self.save),
            ("Save As", "<Control-Shift-S>", self.saveas),
            None,
            ("Add Panel", "<Control-Shift-n>", self.new_panel),
            ("Remove Panel", "<Control-Shift-n>", self.delete_panel),
        )
        self.css = Entry(self.win)

        self.win["bg"] = self.panels["bg"]

        self.menu.pack(side="top", fill="x")
        self.panels.pack(side="bottom", fill="both", expand=True)
        Label(self.win, text="Global Css:").pack(side="left", padx=(20, 10), pady=10)
        self.css.pack(side="right", fill="x", padx=(10, 20), pady=10, expand=True)

        self.open_file = None

    def close(self):
        """Closes the app"""

        if not self.new():
            self.win.destroy()

    def new(self):
        """Loads a new file"""

        if self.open_file is not None:
            option = askyesnocancel("", "Save Work?")

            if option:
                if not self.save():
                    return
            elif option is None:
                return 1

        for i in range(len(self.panels.get_panels())):
            self.panels.delete(0)

        self.css.delete(0, "end")
        self.open_file = None
        self.win.title("")

    def open(self):
        """Ask the user for a file and opens it"""

        file = askopenfilename(defaultextension=".json", filetypes=[("Json file", "*.json"),
                                                                      ("Text file", "*.txt"),
                                                                      ("Any File", "*.*")])

        if file:
            if self.new():
                return

            self.force_open(file)

    def force_open(self, file):
        """Opens a file"""

        try:
            data = json.load(open(file))
        except Exception as err:
            showerror("", "Unable to open file: " + file + "\nReason: " + str(err))
            return

        css = data.pop("", "")
        self.css.delete(0, "end")
        self.css.insert(0, css)

        for name in data:
            n = data[name][0]
            b = Board()
            b.buttons = [i + [None] for i in data[name][1]]
            b.n_cols.insert("end", str(n))
            b.n_buttons.insert("end", str(len(b.buttons)))
            b.refresh_buttons(None)
            self.panels.add(name, b)

        self.open_file = file

        self.win.title(file)

    def save(self):
        """Saves the currently opened file, if no file is opened, it calls save as"""

        if self.open_file is None:
            return self.saveas()

        data = {self.panels.get_label(i): panel.get_data() for i, panel in enumerate(self.panels.get_panels())}
        data[""] = self.css.get()

        try:
            json.dump(data, open(self.open_file, "w"), indent=4)

            return 1
        except Exception as err:
            showerror("", "Unable to open file: " + self.open_file + "\nReason: "+str(err))

    def saveas(self):
        """Ask the user for a file and saves the current file to the file"""

        file = asksaveasfilename(defaultextension=".json", filetypes=[("Json file", "*.json"),
                                                                      ("Text file", "*.txt"),
                                                                      ("Any File", "*.*")])

        if file:
            self.open_file = file

            self.win.title(file)

            return self.save()
        else:
            return 1

    def run(self):
        """Runs mainloop"""

        self.win.mainloop()

    def new_panel(self):
        """Adds a new panel"""

        name = askstring("", "Name:")
        if name:
            for i in range(len(self.panels.get_panels())):
                if name == self.panels.get_label(i):
                    self.panels.select(i)
                    return

            self.panels.add(name, Board())

    def delete_panel(self):
        """Deletes currently selected panel"""

        if askyesno("", "Are you sure you want to delete currently selected panel,\nThis action cannot be undone"):
            if self.panels.current_index is not None:
                self.panels.delete(self.panels.current_index)
