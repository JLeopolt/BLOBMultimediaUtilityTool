from idlelib.tooltip import Hovertip
from tkinter import ttk

from core.gui.main.components import convert_widget, metadata_widget, console, shortcut_panel as shortcuts
from core.tasks import commands

# the main widget
widget: ttk.Frame

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
    # destroy the widget and rebuild it
    widget.destroy()
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
    load_button = ttk.Button(input_frame, text='Load', width=6, command=commands.Load_Async)
    Hovertip(load_button, 'Load source streams from URL.')
    load_button.pack(side='left', padx=3)

    return input_frame
