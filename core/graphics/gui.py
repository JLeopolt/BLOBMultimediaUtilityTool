import tkinter as tk
from tkinter import ttk

import core
from core.graphics.tabs.youtube import youtube_tab


class App(tk.Tk):
    # Tabs for application modes
    blob_tab = None
    yt_tab = None

    def __init__(self):
        super().__init__()

        # root window
        self.title('BLOB Multimedia Utility Tool v' + core.__version__)
        self.geometry('600x700')
        self.style = ttk.Style(self)

        # menubar config
        self.configure_menubar()

        # tab controls
        self.notebook = ttk.Notebook(self)

        # create tabs
        self.blob_tab = ttk.Frame(self.notebook)
        self.youtube_tab = youtube_tab.YoutubeTab()

        # setup notebook
        self.notebook.add(self.blob_tab, text='BLOB')
        self.notebook.add(self.youtube_tab, text='YouTube')
        self.notebook.pack(expand=1, fill="both")

        # label
        label = ttk.Label(self.blob_tab, text='Enter multimedia URL:')
        label.grid(column=0, row=0, padx=10, pady=10, sticky='w')
        # entry
        textbox = ttk.Entry(self.blob_tab)
        textbox.grid(column=1, row=0, padx=10, pady=10, sticky='w')
        # button
        btn = ttk.Button(self.blob_tab, text='Download')
        btn.grid(column=2, row=0, padx=10, pady=10, sticky='w')

    def configure_menubar(self):
        # Create menubar
        menubar = tk.Menu(self)

        # Prepare FileMenu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Prepare HelpMenu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help Index")
        help_menu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help_menu)

        # Add the Menu to window
        self.config(menu=menubar)
