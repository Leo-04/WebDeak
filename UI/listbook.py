from tkinter import *


class ListBook(PanedWindow):
    def __init__(self, *args, **kwargs):
        items_kwargs = {}

        if "font" in kwargs:
            items_kwargs["font"] = kwargs.pop("font")

        if "fg" in kwargs:
            items_kwargs["fg"] = kwargs.pop("fg")

        PanedWindow.__init__(self, *args, **kwargs, sashrelief="raised", showhandle=True, sashwidth=10)
        self.button_frame = Frame(self)

        self.current_index = None
        self.frames = []

        PanedWindow.add(self, self.button_frame, sticky="ns", minsize=100)

    def get_panels(self):
        """Returns array of panels"""

        return self.frames.copy()

    def get_label(self, index):
        """Gets the label at a given index"""

        return self.button_frame.pack_slaves()[index]["text"]

    def delete(self, index):
        """Deletes a panel at a given index"""

        f = self.frames.pop(index)
        f.grid_forget()
        f.destroy()
        f = self.button_frame.pack_slaves()[index]
        f.grid_forget()
        f.destroy()

        if len(self.button_frame.pack_slaves()) == 0:
            self.current_index = None
        else:
            self.select(index - 1)

    def add(self, label, frame):
        """Adds a panel with a given label"""

        self.frames.append(frame)

        button = Button(self.button_frame, text=label)
        button.bind("<ButtonRelease-1>", self.click)
        button.bind("<Leave>", self.stop_leave)
        button.pack(side=TOP, fill=X)

        self.after(100, lambda: self.select(-1))

    def stop_leave(self, event):
        """Stops the leave event on the currently selected button to allow it to stay selected"""

        button = event.widget
        buttons = self.button_frame.pack_slaves()
        index = buttons.index(button)

        if index == self.current_index:
            return "break"

    def click(self, event):
        """One of the sidebar buttons have been clicked"""

        buttons = self.button_frame.pack_slaves()

        self.select(buttons.index(event.widget))

    def select_button(self, index):
        """Puts a button in select mode"""

        buttons = self.button_frame.pack_slaves()
        button = buttons[index]

        for b in buttons:
            b["relief"] = "raised"
            b.event_generate("<Leave>", when="tail")

        button["relief"] = "sunken"
        button.event_generate("<ButtonPress-1>", when="tail")

    def select(self, index):
        """Selects a given index"""

        if self.current_index is not None:
            self.frames[self.current_index].grid_forget()

        for w in self.frames:
            self.remove(w)

        PanedWindow.add(self, self.frames[index], sticky="nsew")

        self.select_button(index)
        self.current_index = index
