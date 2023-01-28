import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from datetime import datetime

import core.__main__


def get_date_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


class Console(tk.scrolledtext.ScrolledText):

    def __init__(self, container):
        super().__init__(container, undo=True)

        # disable manual input
        self.disable()

        # set the font
        self['font'] = ('consolas', '10')
        self.setup_console_tags()

        # Add application information
        self.print(core.__main__.get_software_details())

    def setup_console_tags(self):
        self.tag_configure('error', background="yellow", foreground="red")
        self.tag_configure('warning', background="orange", foreground="white")
        self.tag_configure('success', background="green", foreground="white")
        self.tag_configure('notice', background="blue", foreground="white")

    # Prevents modification of the Text widget, EVEN by the software.
    # Also scrolls to the bottom, since this is usually called after inserting.
    def disable(self):
        self.configure(state='disabled')
        self.see(tk.END)

    # Enables all forms of modification of the Text widget.
    def enable(self):
        self.configure(state='normal')

    def print(self, msg):
        self.enable()
        self.insert('end', msg + "\n")
        self.disable()

    def printHeaderWithTimestamp(self, header, content, tag):
        self.enable()
        self.insert('end', get_date_time() + " " + header + ": " + content + "\n", tag)
        self.disable()

    def printHeaderWithTimestampUntagged(self, header, content):
        self.enable()
        self.insert('end', get_date_time() + " " + header + ": " + content + "\n")
        self.disable()

    def printError(self, content):
        self.printHeaderWithTimestamp("(ERROR)", content, 'error')

    def printSuccess(self, content):
        self.printHeaderWithTimestamp("(SUCCESS)", content, 'success')

    def printInfo(self, content):
        self.printHeaderWithTimestampUntagged("(INFO)", content)

    def printNotice(self, content):
        self.printHeaderWithTimestamp("(NOTICE)", content, 'notice')

    def printWarning(self, content):
        self.printHeaderWithTimestamp("(WARN)", content, 'warning')
