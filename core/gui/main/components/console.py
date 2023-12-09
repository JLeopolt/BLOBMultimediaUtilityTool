import os
import sys
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog

import core.__main__ as mainpy
import core.utility.utils as utils

# Until the start() method is called, the widget is just a placeholder.
widget: tk.scrolledtext.ScrolledText

# used for logging purposes -- whether the console has been cleared since launch.
was_console_cleared = False


# Create the console and add it to the specified container.
def build(parent):
    global widget
    widget = tk.scrolledtext.ScrolledText(parent, undo=True, wrap='word', cursor="")
    widget.pack(side='bottom', expand=True, fill='both')

    # Redirect std to console using TextRedirector class.
    sys.stdout = TextRedirector('stdout')
    sys.stderr = TextRedirector('stderr')

    # set the font
    set_font(('consolas', '10'))

    setup_console_tags()

    print_startup_info()


# opens a GUI dialog allowing the user to change the font used by console.
def open_font_selector():
    widget.tk.call('tk', 'fontchooser', 'configure', '-font', widget['font'], '-command', widget.register(set_font))
    widget.tk.call('tk', 'fontchooser', 'show')


# updates the console font.
def set_font(font):
    widget['font'] = font


def print_startup_info():
    # timestamp of console launch / clear, and python version.
    if was_console_cleared:
        printNotice("Console cleared. (Python " + mainpy.get_python_version() + ")")
    else:
        printNotice("Console started. (Python " + mainpy.get_python_version() + ")")

    # print software / license info.
    printInfo(mainpy.get_software_details() + "\n" + mainpy.get_license_details())


# creates all the console 'tags' which are color schemes for the text. Used to highlight errors, info, success, etc.
def setup_console_tags():
    widget.tag_configure('error', background="yellow", foreground="red")
    widget.tag_configure('warning', background="orange")
    widget.tag_configure('success', background="green", foreground="white")
    widget.tag_configure('notice', background="blue", foreground="white")

    widget.tag_configure('stdout', background="white", foreground="blue")
    widget.tag_configure('stderr', background="white", foreground="red")

    widget.tag_configure('link-open-file', background="purple", foreground="white", underline=True, justify='center')
    widget.tag_bind('link-open-file', '<Button-1>', link_open_file_location)

    # selection highlight should take priority over tags.
    widget.tag_raise("sel")


def link_open_file_location(event):
    location = event.widget.tag_names('current')[1]

    # ignore selections
    if location == 'sel':
        return

    # open the file in explorer
    os.system('explorer /select,\"' + location.replace('/', '\\') + "\"")


# saves the console history to a file.
def save_log():
    # possible file types to allow
    file_types = [('MUD Log', '*.mudlog'),
                  ('Text Document', '*.txt'),
                  ('All Files', '*.*')]

    # save as a .log file, named MUD-Log-<time date>.log by default.
    # returns file
    file = filedialog.asksaveasfile(initialdir=os.getcwd(),
                                    title='Save Console Log',
                                    defaultextension='*.mudlog',
                                    filetypes=file_types,
                                    initialfile="MUD-Log-" + utils.get_date_time().replace("/", "-")
                                    .replace(" ", "-")
                                    .replace(":", "-"))

    # if cancelled save operation
    if file is None:
        printWarning('Cancelled save console log operation.')
        return

    # write the widget contents to the file
    file.write(widget.get("1.0", 'end'))
    file.close()

    # inform the user that the log was saved.
    printInfo('Saved console log as \"' + str(file.name) + "\"")


# Prevents modification of the Text widget, EVEN by the software.
# Also scrolls to the bottom, since this is usually called after inserting.
def disable():
    widget.configure(state='disabled')
    widget.see(tk.END)


# Enables all forms of modification of the Text widget.
def enable():
    widget.configure(state='normal')


# Clears the entire console, then reposts the software details info.
def clear():
    global was_console_cleared
    was_console_cleared = True

    enable()
    widget.delete('1.0', 'end')
    print_startup_info()


def addHyperlinkOpenFile(text, file_location):
    enable()
    widget.insert('end', "\n" + text + "\n\n", ('link-open-file', file_location))
    disable()


def printHeaderWithTimestamp(header, content, tag):
    enable()
    widget.insert('end', utils.get_date_time() + " " + header + ": " + content + "\n", tag)
    disable()


def printHeaderWithTimestampUntagged(header, content):
    enable()
    widget.insert('end', utils.get_date_time() + " " + header + ": " + content + "\n")
    disable()


# the console will print the output with 'stdout' or 'stderr' as the header / tag.
def printStdOutput(stdType, content):
    if utils.trim(content) is None or "":
        return
    enable()
    widget.insert('end', utils.get_date_time() + " " + content + "\n", stdType)
    disable()


def printError(content):
    printHeaderWithTimestamp("(ERROR)", content, 'error')


def printSuccess(content):
    printHeaderWithTimestamp("(SUCCESS)", content, 'success')


def printInfo(content):
    printHeaderWithTimestampUntagged("(INFO)", content)


def printNotice(content):
    printHeaderWithTimestamp("(NOTICE)", content, 'notice')


def printWarning(content):
    printHeaderWithTimestamp("(WARN)", content, 'warning')


# used to redirect std output to the console.
class TextRedirector(object):
    def __init__(self, tag="stdout"):
        self.hide_end = False
        self.tag = tag

    # called by stdout/stderr when writing python console output to widget.
    def write(self, std):
        # since print() statements call write() twice, ignore every Second write() call.
        if not self.hide_end:
            printStdOutput(self.tag, std)
            self.hide_end = True
        else:
            self.hide_end = False

    def flush(self):
        pass
