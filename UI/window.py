# ====================================================================================
#                                       Window
# This class creates the main window
# It allows me to set is icon & closing function
# It also allows me to set the viability of the window with `hide` and `show`
#
# ====================================================================================

from tkinter import *


class Window(Tk):
    def __init__(self, title="My App", on_close_callback=None):
        # Set up window
        Tk.__init__(self)
        self.base_title = title
        self.title("")
        self.geometry("600x600")
        self.minsize(400, 400)

        self.on_close(on_close_callback)

    def on_close(self, on_close_callback):
        """Sets the callback function for when the window closes"""

        if on_close_callback is not None:
            # Check if its a function
            if not callable(on_close_callback):
                raise TypeError("on_close_callback should be a function")

            self.protocol("WM_DELETE_WINDOW", on_close_callback)
        else:
            self.protocol("WM_DELETE_WINDOW", self.destroy)

    def title(self, title=None, ext=" - "):
        """Sets the title of the window"""

        if title is None:
            return Tk.title(self)
        elif title == "":
            Tk.title(self, self.base_title)
        else:
            Tk.title(self, self.base_title + ext + title)

    def hide(self):
        """Hides the window from view"""

        self.withdraw()

    def show(self):
        """Shows the window"""

        self.deiconify()
        self.update()

    def set_icon(self, base64data: bytes):
        """
        Set the icon of the tkinter window from a base 64 byte array
        """

        if not isinstance(base64data, bytes):
            raise TypeError("base64data is not bytes")

        # Call internal tlc command
        self.tk.call('wm', 'iconphoto', self._w, PhotoImage(data=base64data))

