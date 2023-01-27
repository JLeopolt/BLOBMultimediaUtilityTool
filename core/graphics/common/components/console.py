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
        self.bind("<Key>", lambda e: "break")

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

    def print(self, msg):
        self.insert('end', msg + "\n")

    def printError(self, error_text):
        self.insert('end', "(ERROR) " + get_date_time() + ": " + error_text + "\n", 'error')

    def printSuccess(self, success_msg):
        self.insert('end', "(SUCCESS) " + get_date_time() + ": " + success_msg + "\n", 'success')

    def printInfo(self, info):
        self.insert('end', "(INFO) " + get_date_time() + ": " + info + "\n")

    def printNotice(self, msg):
        self.insert('end', "(NOTICE) " + get_date_time() + ": " + msg + "\n", 'notice')

    def printWarning(self, msg):
        self.insert('end', "(WARN) " + get_date_time() + ": " + msg + "\n", 'warning')
