import tkinter as tk
from tkinter import ttk

import core
from core.graphics.tabs.youtube import tab


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

        # tab controls
        self.notebook = ttk.Notebook(self)

        # create tabs
        self.blob_tab = ttk.Frame(self.notebook)
        self.youtube_tab = tab.YoutubeTab()

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

        # menubar config
        self.configure_menubar()

    def configure_menubar(self):
        # Create menubar
        menubar = tk.Menu(self)

        # Prepare 'File' menu
        file_menu = tk.Menu(menubar, tearoff=0)

        # 'Styles' submenu
        themes_submenu = tk.Menu(file_menu, tearoff=0)
        # Add all theme options
        for theme_name in self.style.theme_names():
            themes_submenu.add_command(label=theme_name, command=lambda t=theme_name: self.style.theme_use(t))
        file_menu.add_cascade(label="Styles", menu=themes_submenu)
        # clears the console
        file_menu.add_command(label="Clear Console", command=self.youtube_tab.console.clear)

        file_menu.add_separator()
        # exits the program
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Prepare HelpMenu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help_menu)

        # Add the Menu to window
        self.config(menu=menubar)
