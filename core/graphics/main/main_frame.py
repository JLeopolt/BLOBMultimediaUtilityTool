from idlelib.tooltip import Hovertip
from threading import Thread
from tkinter import ttk
from core.services import loader
from core.graphics.common import console as cs, utils
from core.graphics.main import scontrols as shortcuts
from core.graphics.main.modules import convert_frame, metadata_frame as metadata


# noinspection PyAttributeOutsideInit
class MainFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)

        # must be initialized on startup
        self.worker_thread = None

        # Prepare the console before packing it
        self.console_frame = ttk.LabelFrame(self, text='Console')
        self.console = cs.Console(self.console_frame)
        self.console.pack(side='bottom', expand=True, fill='both')

        self.build()

    def build(self):
        # Prepare the input frame
        input_frame = self.build_input_frame()
        input_frame.pack(side='top', fill='x', anchor='n')

        # Houses youtube video metadata
        self.metadata_frame = metadata.MetadataFrame(self)
        self.metadata_frame.pack(side='top', fill='x', anchor='n')

        # houses download streams, conversion options
        self.convert_frame = convert_frame.ConvertFrame(self, self.console)
        self.convert_frame.pack(side='top', fill='x', anchor='n')

        # pack the console at the bottom
        self.console_frame.pack(side='bottom', expand=True, fill='both')

    # hides all video metadata, convert tab, etc. Console and settings remain unchanged.
    def Clear(self):
        # perform graceful reset for certain frames
        self.metadata_frame.reset()
        self.convert_frame.reset()

        # repack everything
        utils.pack_forget_children(self)
        self.build()

    # returns all the input controls in a single Frame.
    def build_input_frame(self):
        # Instantiate the full frame
        input_frame = ttk.LabelFrame(self, text='Shortcuts')

        self.short_cuts = shortcuts.Shortcuts(self, input_frame)
        self.short_cuts.pack(side='top', fill='x')

        # Label for input field
        url_label = ttk.Label(input_frame, text='URL:')
        url_label.pack(side='left', padx=3)

        # url entry field
        self.link_entry_field = ttk.Entry(input_frame)
        self.link_entry_field.pack(side='left', padx=3, expand=True, fill='x')

        # load button
        load_button = ttk.Button(input_frame, text='Load', width=6, command=self.schedule_load_media)
        Hovertip(load_button, 'Load source streams from URL.')
        load_button.pack(side='left', padx=3)

        return input_frame

    # Schedules to asynchronously load a media, using the task param as the function
    # automatically determines which URL Mode to use.
    def schedule_load_media(self):
        # cancel if a process is alr occurring.
        if self.worker_thread is not None and self.worker_thread.is_alive():
            self.console.printError('Please wait for the current process to finish before scheduling a new process.')
            return

        # determine which function to call
        self.worker_thread = None

        # load the media on a worker thread
        self.worker_thread = Thread(target=loader.load, args=[self])
        self.worker_thread.start()
