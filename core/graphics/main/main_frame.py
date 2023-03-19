from idlelib.tooltip import Hovertip
from threading import Thread
from tkinter import ttk

from core.graphics.common import console, utils
from core.graphics.main import shortcut_panel as shortcuts
from core.graphics.main.modules import convert_widget, metadata_widget
from core.services import loader

# the main widget
widget: ttk.Frame

# the thread which will perform any async task, one at a time.
worker_thread = None

# the entry field which contains the url
link_entry_field: ttk.Entry


def build(parent):
    global widget
    widget = ttk.Frame(parent)
    widget.pack(expand=True, fill='both')

    # Prepare the console frame, then build the console component.
    # The console must be initialized, but isn't packed until the end.
    console_container = ttk.LabelFrame(widget, text='Console')
    console.build(console_container)

    # Prepare the input frame
    input_frame = build_input_frame()
    input_frame.pack(side='top', fill='x', anchor='n')

    # Displays metadata about the media file.
    metadata_widget.build(widget)

    # houses download streams, conversion options
    convert_widget.build(widget)

    # pack the console at the bottom, do this LAST
    console_container.pack(side='bottom', expand=True, fill='both')


# hides all video metadata, convert tab, etc. Console and settings remain unchanged.
def clear():
    # perform graceful reset for certain frames
    metadata_widget.reset()
    convert_widget.reset()

    # repack everything
    utils.pack_forget_children(widget)
    build(widget.master)


# returns all the input controls in a single Frame.
def build_input_frame():
    # Instantiate the full frame
    input_frame = ttk.LabelFrame(widget, text='Shortcuts')

    # shortcut button panel
    shortcuts.build(input_frame)

    # Label for input field
    url_label = ttk.Label(input_frame, text='URL:')
    url_label.pack(side='left', padx=3)

    # url entry field
    global link_entry_field
    link_entry_field = ttk.Entry(input_frame)
    link_entry_field.pack(side='left', padx=3, expand=True, fill='x')

    # load button
    load_button = ttk.Button(input_frame, text='Load', width=6, command=schedule_load_media)
    Hovertip(load_button, 'Load source streams from URL.')
    load_button.pack(side='left', padx=3)

    return input_frame


# Schedules to asynchronously load a media, using the task param as the function
# automatically determines which URL Mode to use.
def schedule_load_media():
    global worker_thread

    # cancel if a process is alr occurring.
    if worker_thread is not None and worker_thread.is_alive():
        console.printError('Please wait for the current process to finish before scheduling a new process.')
        return

    # load the media on a worker thread
    worker_thread = Thread(target=loader.load, args=[])
    worker_thread.start()
