from tkinter import *

from UI.intentry import IntEntry


class Board(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs, relief="sunken")
        self.n_cols = IntEntry(self)
        self.n_buttons = IntEntry(self)

        self.n_cols.bind("<<Updated>>", self.refresh_buttons)
        self.n_buttons.bind("<<Updated>>", self.refresh_buttons)

        self.button_frame = Frame(self, padx=40, pady=40)
        self.vcmd = (self.register(self.on_edit))
        self.name = Entry(self)
        self.command = Entry(self)
        self.css = Entry(self)
        self.img = Entry(self)

        self.name.bind("<KeyRelease>", self.on_edit)
        self.command.bind("<KeyRelease>", self.on_edit)
        self.css.bind("<KeyRelease>", self.on_edit)
        self.img.bind("<KeyRelease>", self.on_edit)

        Label(self, text="Number Of Columns:").grid(row=0, column=0, padx=(20, 0))
        self.n_cols.grid(row=0, column=1, sticky="ew", pady=10)
        Label(self, text="Number Of Buttons:").grid(row=0, column=2, padx=(20, 0))
        self.n_buttons.grid(row=0, column=3, sticky="ew", pady=10, padx=(0, 20))
        self.button_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")
        Label(self, text="Label:").grid(row=2, column=0, padx=(20, 0))
        self.name.grid(row=2, column=1, sticky="ew", columnspan=3, padx=(0, 20), pady=10)
        Label(self, text="Command Line:").grid(row=3, column=0, padx=(20, 0))
        self.command.grid(row=3, column=1, sticky="ew", columnspan=3, padx=(0, 20), pady=10)
        Label(self, text="CSS Style:").grid(row=4, column=0, padx=(20, 0))
        self.css.grid(row=4, column=1, sticky="ew", columnspan=3, padx=(0, 20), pady=10)
        Label(self, text="Image Location:").grid(row=5, column=0, padx=(20, 0))
        self.img.grid(row=5, column=1, sticky="ew", columnspan=3, padx=(0, 20), pady=10)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(1, weight=1)

        self.buttons = []
        self.selected_button = None

    def on_edit(self, event=None):
        """Update information when it is edited"""

        if self.selected_button is not None:
            name = self.name.get()
            self.buttons[self.selected_button][0] = name
            self.buttons[self.selected_button][1] = self.command.get()
            self.buttons[self.selected_button][2] = self.css.get()
            self.buttons[self.selected_button][3]=self.img.get()
            self.buttons[self.selected_button][4]["text"] = name
            try:
                self.buttons[self.selected_button][4].image.config(file=self.img.get())
            except TclError:
                pass

        return True

    def refresh_buttons(self, event=None):
        """Update the information displayed on the buttons"""

        for row_num in range(self.button_frame.grid_size()[1]):
            self.button_frame.rowconfigure(row_num, weight=0)
        for row_num in range(self.button_frame.grid_size()[0]):
            self.button_frame.columnconfigure(row_num, weight=0)

        for button in self.button_frame.grid_slaves():
            button.grid_forget()
            button.destroy()

        n_cols = self.n_cols.get()
        x = y = 0
        for i in range(self.n_buttons.get()):
            if len(self.buttons) >= i:
                self.buttons.append(["", "", "", "", None])

            button = Button(self.button_frame, text=self.buttons[i][0],
                            command=lambda index=i: self.select_button(index))
            button.grid(row=y, column=x, sticky="nsew")
            button.image = PhotoImage()
            button.config(image=button.image, compound="top")

            self.button_frame.columnconfigure(x, weight=1)
            self.button_frame.rowconfigure(y, weight=1)
            self.buttons[i][4] = button

            try:
                button.image.config(file=self.buttons[i][3])
            except TclError:
                pass

            x += 1

            if x >= n_cols:
                x = 0
                y += 1

    def select_button(self, index):
        """Select a button for editing"""

        text, cmd, css, img, button = self.buttons[index]

        self.name.delete(0, "end")
        self.name.insert(0, text)
        self.command.delete(0, "end")
        self.command.insert(0, cmd)
        self.css.delete(0, "end")
        self.css.insert(0, css)
        self.img.delete(0, "end")
        self.img.insert(0, img)

        try:
            button.image.config(file=img)
        except TclError:
            pass

        self.selected_button = index

    def get_data(self):
        """Returns data"""

        return self.n_cols.get(), [(name, cmd, css, img) for name, cmd, css, img, button in self.buttons[:self.n_buttons.get()]]
