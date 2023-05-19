from tkinter import Entry


class IntEntry(Entry):
    def __init__(self, *args, min=0, max=100, **kwargs):
        Entry.__init__(self, *args, **kwargs)
        self.vcmd = (self.register(self.validate))
        self.config(validatecommand=(self.vcmd, '%P'), validate='all')
        self.min = min
        self.max = max

    def validate(self, string):
        """Only allows integers between self.min and self.max"""

        self.event_generate("<<Updated>>", when="tail")
        if string == "":
            return True
        elif string.isdigit():
            num = int(string)

            return self.min <= num <= self.max
        else:
            return False

    def get(self) -> int:
        """Gets the value as a integer"""

        value = Entry.get(self)

        if value == "":
            return 0

        return int(value)
