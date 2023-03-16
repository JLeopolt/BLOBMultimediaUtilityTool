import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from datetime import datetime

import sys

import core.__main__


def get_date_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


class Console(tk.scrolledtext.ScrolledText):

    def __init__(self, container):
        super().__init__(container, undo=True, wrap='word')

        # disable manual input
        self.disable()

        # set the font
        self['font'] = ('consolas', '10')
        self.setup_console_tags()

        # Add application information
        self.print(core.__main__.get_software_details())

    def setup_console_tags(self):
        self.tag_configure('error', background="yellow", foreground="red")
        self.tag_configure('warning', background="orange")
        self.tag_configure('success', background="green", foreground="white")
        self.tag_configure('notice', background="blue", foreground="white")

        self.tag_configure('stdout', background="white", foreground="blue")
        self.tag_configure('stderr', background="white", foreground="red")

        # selection should show up always
        self.tag_raise("sel")

    # Prevents modification of the Text widget, EVEN by the software.
    # Also scrolls to the bottom, since this is usually called after inserting.
    def disable(self):
        self.configure(state='disabled')
        self.see(tk.END)

    # Enables all forms of modification of the Text widget.
    def enable(self):
        self.configure(state='normal')

    # Clears the entire console, then reposts the software details info.
    def clear(self):
        self.enable()
        self.delete('1.0', 'end')
        self.print(core.__main__.get_software_details())

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

    # the console will print the output with 'stdout' or 'stderr' as the header / tag.
    def printConsoleOutput(self, stdType, content):
        if content == '\n':
            return
        self.enable()
        self.insert('end', get_date_time() + " " + stdType + ": " + content + "\n", stdType)
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


# used to redirect std output to the console.
class TextRedirector(object):
    def __init__(self, console, tag="stdout"):
        self.console = console
        self.tag = tag

    # called by stdout/stderr when writing python console output to widget.
    def write(self, std):
        self.console.printConsoleOutput(str(self.tag), std)

    def flush(self):
        pass
