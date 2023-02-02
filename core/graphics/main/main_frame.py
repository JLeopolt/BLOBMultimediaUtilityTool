import time
from idlelib.tooltip import Hovertip
from threading import Thread
from tkinter import ttk
from pytube.exceptions import RegexMatchError
import core.services.youtube
from core.graphics.common import console as cs, utils
from core.graphics.main import scontrols as shortcuts
from core.graphics.main.modules import convert_frame, metadata_frame


# noinspection PyAttributeOutsideInit
class MainFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)

        # must be initialized on startup
        self.worker_thread = None

        # Prepare the console before packing it console
        self.console_frame = ttk.LabelFrame(self, text='Console')
        self.console = cs.Console(self.console_frame)
        self.console.pack(side='bottom', expand=True, fill='both')

        self.build()

    def build(self):
        # Prepare the input frame
        input_frame = self.build_input_frame()
        input_frame.pack(side='top', fill='x', anchor='n')

        # Houses youtube video metadata
        self.youtube_metadata_frame = metadata_frame.MetadataFrame(self)
        self.youtube_metadata_frame.pack(side='top', fill='x', anchor='n')

        # houses download streams, conversion options
        self.convert_frame = convert_frame.ConvertFrame(self)
        self.convert_frame.pack(side='top', fill='x', anchor='n')

        # pack the console at the bottom
        self.console_frame.pack(side='bottom', expand=True, fill='both')

    # hides all video metadata, convert tab, etc. Console and settings remain unchanged.
    def Clear(self):
        # perform graceful reset for certain frames
        self.youtube_metadata_frame.reset()
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
        load_button = ttk.Button(input_frame, text='Load', width=6, command=self.schedule_youtube_video_access)
        Hovertip(load_button, 'Load source streams from URL.')
        load_button.pack(side='left', padx=3)

        return input_frame

    # Schedules to async load the YouTube streams.
    def schedule_youtube_video_access(self):
        # cancel if a process is alr occurring.
        if self.worker_thread is not None and self.worker_thread.is_alive():
            self.console.printError('Please wait for the current process to finish before scheduling a new process.')
            return

        # if free to start a new process, do so on a worker thread.
        self.worker_thread = Thread(target=self.load_youtube_video)
        self.worker_thread.start()

    def load_youtube_video(self):
        # Get the YouTube link from user input
        youtube_link = self.link_entry_field.get()
        if utils.trim(youtube_link) == '':
            self.console.printError("No link was provided.")
            return

        self.short_cuts.block_new_processes()

        # Start the progress bar
        start_time = time.time()

        # Get the metadata here.
        try:
            youtube = core.services.youtube.get_YouTube_object(youtube_link)
        except RegexMatchError:
            self.console.printError("Input is not a valid URL.")
            self.short_cuts.unblock_new_processes()
            return
        except (Exception,) as e:
            self.console.printError(str(e))
            self.short_cuts.unblock_new_processes()
            return

        # resets, then builds the metadata frame
        self.youtube_metadata_frame.build(youtube)

        mid_time = time.time()
        self.console.printInfo("Accessed video metadata. (" + str(round(mid_time - start_time, 2)) + "s)")
        self.console.printInfo("Retrieving download streams..")

        # Access the download streams here.
        # Readies the Converter frame.
        self.convert_frame.build(youtube=youtube)

        # Success message to notify the user
        self.console.printSuccess("Retrieved all available download streams for \"" + youtube.title + "\" ("
                                  + str(round(time.time() - mid_time, 2)) + "s).")

        # Unblock shortcuts
        self.short_cuts.unblock_new_processes()
