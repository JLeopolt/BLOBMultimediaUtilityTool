import core
import core.services.youtube
import tkinter as tk
from tkinter import ttk


class App(tk.Tk):

    yt_notebook = None
    yt_tabs = None
    yt_entry_box = None

    def display_youtube_download_options(self, youtube):
        # Add all Video download options
        for source in youtube.streams.filter():
            rb = ttk.Button(
                self.yt_tabs[0],
                text=source.mime_type
            )
            rb.pack(expand=True, fill='both')

    def download_youtube_video(self):
        youtube_link = self.yt_entry_box.get()
        if youtube_link is None:
            return
        youtube = core.services.youtube.get_YouTube_object(youtube_link)
        self.display_youtube_download_options(youtube)

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

    def setup_youtube_tab(self):
        # label
        label = ttk.Label(self.youtube_tab, text='Enter YouTube URL:')
        label.grid(column=0, row=0, padx=10, pady=10, sticky='w')
        # entry
        self.yt_entry_box = ttk.Entry(self.youtube_tab)
        self.yt_entry_box.grid(column=1, row=0, padx=10, pady=10, sticky='w')
        # button
        btn = ttk.Button(self.youtube_tab, text='Download', command=self.download_youtube_video)
        btn.grid(column=2, row=0, padx=10, pady=10, sticky='w')

        # Tab label
        download_type_frame = ttk.LabelFrame(self.youtube_tab, text='Download Type')
        download_type_frame.grid(column=0, columnspan=3, padx=100, pady=100, sticky='w')

        # Create Notebook and Tabs
        self.yt_notebook = ttk.Notebook(download_type_frame)
        yt_notebook = self.yt_notebook
        self.yt_tabs = []
        video_tab = ttk.Frame(yt_notebook)
        self.yt_tabs.append(video_tab)
        audio_tab = ttk.Frame(yt_notebook)
        self.yt_tabs.append(audio_tab)

        # Set up the Notebook
        yt_notebook.add(video_tab, text='Video')
        yt_notebook.add(audio_tab, text='Audio')
        yt_notebook.grid(padx=10, pady=10, ipadx=20, ipady=20, sticky='w')

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
        self.tabs = []
        self.blob_tab = ttk.Frame(self.notebook)
        self.tabs.append(self.blob_tab)
        self.youtube_tab = ttk.Frame(self.notebook)
        self.tabs.append(self.youtube_tab)

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

        self.setup_youtube_tab()
