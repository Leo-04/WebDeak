import json
from tkinter import Button, Text, Label
from tkinter.messagebox import showerror
import os
import sys

from UI.intentry import IntEntry
from UI.window import Window
from UI.app import App

from server.server import ServerThread


class Menu:
    def __init__(self, button_grid_path, index_path, error_path, access_denied_path, layout_path, whitelist_path,
                 style_path):
        self.layout_path = layout_path
        self.whitelist_path = whitelist_path
        self.button_grid_path = button_grid_path
        self.index_path = index_path
        self.error_path = error_path
        self.access_denied_path = access_denied_path

        if not os.path.exists(self.layout_path):
            try:
                with open(self.layout_path, "w") as fp:
                    fp.write('{"": ""}')
            except Exception as err:
                showerror("", f"Cannot access file: {self.layout_path}\nReason: {err}")
                return

        if not os.path.exists(self.whitelist_path):
            try:
                with open(self.whitelist_path, "w") as fp:
                    fp.write("0.0.0.0\n")
            except Exception as err:
                showerror("", f"Cannot access file: {self.whitelist_path}\nReason: {err}")
                return

        try:
            with open(self.whitelist_path) as fp:
                ips = fp.read()
        except Exception as err:
            showerror("", f"Cannot access file: {self.whitelist_path}\nReason: {err}")
            return

        self.app = App(style_path)
        self.app.win.hide()
        self.app.win.on_close(lambda: (
            None
            if self.app.new() else (
                self.app.win.hide(),
                self.win.show()
            )
        ))
        self.app.win.hide()

        self.win = Window("WebSD", self.close)
        self.win.minsize(400, 400)
        self.win.geometry("300x400")
        self.win.resizable(False, False)
        self.win.title("Menu")

        try:
            self.win.option_readfile(style_path)
        except:
            pass

        self.edit_button = Button(self.win, text="Edit Buttons", command=self.edit)
        self.run_button = Button(self.win, text="Run Server", command=self.run_server, bg="green")
        self.stop_button = Button(self.win, text="Stop Server", state="disabled", command=self.stop_server)
        self.log = Text(self.win, font="consolas 7", height=1, state="disabled")
        self.port = IntEntry(self.win, min=0, max=65535)
        self.port.insert(0, "8080")
        self.whitelist_label = Label(self.win, text="Whitelist:")
        self.ips = Text(self.win, font="consolas 10", width=3 + 1 + 3 + 1 + 3 + 1 + 3, height=1)
        self.ips.insert("end", ips)
        self.ips.bind("<KeyRelease>", self.save_white_list)
        self.win["bg"] = self.whitelist_label["bg"]

        self.port.grid(sticky="nsew", row=0, column=2, padx=(20, 10), pady=10)
        self.edit_button.grid(sticky="nsew", row=2, column=1, padx=(20, 10), pady=(0, 10))
        self.run_button.grid(sticky="nsew", row=3, column=1, padx=(20, 10), pady=10)
        self.stop_button.grid(sticky="nsew", row=4, column=1, padx=(20, 10), pady=10)

        Label(self.win, text="Port:").grid(sticky="ew", row=0, column=1, padx=(20, 10))
        self.whitelist_label.grid(sticky="nsew", row=1, column=2, pady=0, padx=(10, 20))
        self.ips.grid(row=2, column=2, sticky="nsew", padx=(10, 20), pady=(10, 20), rowspan=3)
        self.log.grid(row=5, column=1, sticky="nsew", padx=(10, 20), pady=(10, 20), columnspan=2)

        self.win.columnconfigure(2, weight=1)
        self.win.rowconfigure(5, weight=1)

        class Writer:
            write = lambda text: self.write(text, "text")

        sys.stdout = Writer()

        class Writer:
            write = lambda text: self.write(text, "error")

        sys.stderr = Writer()

        self.server = ServerThread()

        self.log.tag_config("text", foreground="green")
        self.log.tag_config("error", foreground="red")

    def write(self, text, tag=""):
        """Writes data to the log window"""

        self.log["state"] = "normal"
        self.log.insert('end', text, tag)
        self.log.see('end')
        self.log["state"] = "disabled"

    def save_white_list(self, event=None):
        """Saves the entered IPs to the file"""

        with open(self.whitelist_path, "w") as fp:
            fp.write(self.ips.get("1.0", "end-1c"))

    def edit(self):
        """Opens the edit buttons window and hides the menu window"""

        self.win.hide()
        self.app.force_open(self.layout_path)
        self.app.win.show()

    def run_server(self):
        """Runs a new instance of the server"""

        self.run_button["state"] = "disabled"
        self.run_button["bg"] = self.edit_button["bg"]
        self.stop_button["state"] = "normal"
        self.stop_button["bg"] = "red"
        self.ips["state"] = "disabled"
        self.port["state"] = "disabled"
        self.win.title("RUNNING")

        try:
            with open(self.button_grid_path) as fp:
                page_html = fp.read()
        except Exception as err:
            return showerror("", f"Unable to open file: {self.button_grid_path}\nReason {err}")

        try:
            with open(self.index_path) as fp:
                index_html = fp.read()
        except Exception as err:
            return showerror("", f"Unable to open file: {self.index_path}\nReason {err}")

        try:
            with open(self.error_path) as fp:
                error_html = fp.read()
        except Exception as err:
            return showerror("", f"Unable to open file: {self.error_path}\nReason {err}")

        try:
            with open(self.access_denied_path) as fp:
                access_denied = fp.read()
        except Exception as err:
            return showerror("", f"Unable to open file: {self.access_denied_path}\nReason {err}")

        try:
            layout = json.load(open(self.layout_path))
        except Exception as err:
            return showerror("", f"Unable to open file: {self.layout_path}\nReason {err}")

        self.server.start(layout, page_html, index_html, error_html, access_denied,
                          self.ips.get("1.0", "end-1c").split("\n"), port=self.port.get())

    def stop_server(self):
        """Stops the current instance of the server"""

        self.stop_button["state"] = "disabled"
        self.stop_button["bg"] = self.edit_button["bg"]
        self.run_button["state"] = "normal"
        self.run_button["bg"] = "green"
        self.ips["state"] = "normal"
        self.port["state"] = "normal"
        self.win.title("stopped")

        self.server.stop()

    def close(self):
        """Closes the aplication"""

        self.server.active = False
        self.server.running = False

        self.app.win.destroy()
        self.win.destroy()

    def run(self):
        """Calls mainloop"""

        try:
            self.win.mainloop()
        except:
            pass
