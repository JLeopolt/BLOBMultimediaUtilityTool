import time
import tkinter as tk
import urllib
from idlelib.tooltip import Hovertip
from tkinter import ttk
from urllib import request

from PIL import Image, ImageTk
from pytube.exceptions import RegexMatchError

import core.services.youtube
from core.graphics.common import console as cs, progressbar, utils
from core.graphics.tabs.youtube import scontrols as shortcuts
from core.graphics.tabs.youtube.modules import dl_opts as mdlopts
from core.services import thread


class YoutubeTab(ttk.Frame):
    # Entry box for the YouTube link
    link_entry_field = None

    # the output frame
    output_frame = None

    # The frame which contains the currently selected YouTube video's metadata
    youtube_metadata_frame = None

    more_dl_options = None

    # The option-menus for more download options, 'Video' and 'Audio'
    video_more_dls_frame = None
    audio_more_dls_frame = None

    progress_bar = None

    # Console for debugging
    console = None

    # Cached thumbnails, maintain reference so they don't disappear
    cached_thumbnails = []

    def __init__(self):
        super().__init__()

        self.thread_manager = thread.ThreadManager()

        # Build the console, but pack it last.
        console_frame = self.build_console()

        # Prepare the input frame
        input_frame = self.build_input_frame()
        input_frame.pack(side='top', fill='x', anchor='n')

        # Instantiate, then Populate the output frame
        self.output_frame = self.populate_output_frame(ttk.LabelFrame(self, text='Output'))
        self.output_frame.pack(side='top', fill='x', anchor='n')

        console_frame.pack(side='bottom', expand=True, fill='both')

    # returns all the input controls in a single Frame.
    def build_input_frame(self):
        # Instantiate the full frame
        input_frame = ttk.LabelFrame(self, text='Input')

        rich_control_frame = shortcuts.Shortcuts(self, input_frame)
        rich_control_frame.pack(side='top', fill='x')

        # Label for input field
        url_label = ttk.Label(input_frame, text='YouTube URL:')
        url_label.pack(side='left', padx=3)

        # url entry field
        self.link_entry_field = ttk.Entry(input_frame)
        self.link_entry_field.pack(side='left', padx=3, expand=True, fill='x')

        # load button
        load_button = ttk.Button(input_frame, text='Load', width=6, command=self.schedule_youtube_video_access)
        Hovertip(load_button, '@Load: Loads the YouTube video from URL.')
        load_button.pack(side='left', padx=3)

        # photoimage = tk.PhotoImage(file="core/assets/orrin.png")
        # imgbutton = tk.Button(input_frame, image=photoimage)
        # self.cached_thumbnails.append(photoimage)
        # imgbutton.pack()

        return input_frame

    # Returns the placeholder frame where YouTube video metadata and download options are shown.
    def populate_output_frame(self, output_frame):
        # placeholder for progress bar.
        self.progress_bar = progressbar.ProgressBar(output_frame)
        self.progress_bar.pack(side='top', expand=True, fill='x', anchor='nw')

        # Metadata frame
        self.youtube_metadata_frame = ttk.LabelFrame(output_frame, text='Metadata')
        self.youtube_metadata_frame.pack(side='left', expand=True, fill='both', anchor='nw')

        # Download Options frame
        self.more_dl_options = mdlopts.MoreDownloadOptions(output_frame, console=self.console)
        self.more_dl_options.pack(side='right', fill='x', anchor='n')

        return output_frame

    # Returns a frame with the console.
    def build_console(self):
        # Instantiate the frame
        console_frame = ttk.LabelFrame(self, text='Console')

        self.console = cs.Console(console_frame)
        self.console.pack(side='bottom', expand=True, fill='both')

        return console_frame

    def reset_output_frame(self):
        utils.destroy_children(self.output_frame)
        self.populate_output_frame(self.output_frame)

    # Schedules to async load the YouTube streams.
    def schedule_youtube_video_access(self):
        self.reset_output_frame()
        self.thread_manager.schedule(target=self.load_youtube_video)

    # event should be the revocable thread's canceller event, automatically passed in by RevocableThread.
    def load_youtube_video(self, event):
        # Get the YouTube link from user input
        youtube_link = self.link_entry_field.get()
        if utils.trim(youtube_link) == '':
            self.console.printError("No link was provided.")
            return

        # Start the progress bar
        self.progress_bar.start()
        start_time = time.time()

        # Get the stream from pytube after getting the link.
        try:
            youtube = core.services.youtube.get_YouTube_object(youtube_link)
        except RegexMatchError:
            self.console.printError("Input is not a valid URL.")
            return
        except (Exception,) as e:
            self.console.printError(str(e))
            return

        self.update_youtube_metadata_frame(youtube)

        mid_time = time.time()
        self.console.printInfo("Accessed video metadata. (" + str(round(mid_time - start_time, 2)) + "s)")
        self.console.printInfo("Retrieving download streams..")

        # Access the download streams here.
        youtube.streams.filter()

        # stop the progress bar
        self.progress_bar.stop()

        # If the event is set, this thread was 'cancelled'. Do nothing with the YouTube stream, just return.
        if event.is_set():
            return

        # Success message to notify the user
        self.console.printSuccess("Retrieved all available download streams for \"" + youtube.title + "\" ("
                                  + str(round(time.time() - mid_time, 2)) + "s).")

        self.more_dl_options.show_options(youtube)

    # Updates the YouTube metadata frame with video's thumbnail, title, and duration.
    def update_youtube_metadata_frame(self, youtube):
        # The thumbnail image
        thumbnail_image = self.get_youtube_thumbnail(youtube.thumbnail_url)
        thumbnail = ttk.Label(self.youtube_metadata_frame, image=thumbnail_image)
        thumbnail.pack(side='left', anchor='nw')

        # Video metadata
        metadata = tk.Frame(self.youtube_metadata_frame)
        metadata.pack(side='left', anchor='nw')
        tk.Label(metadata, text="\"" + youtube.title + "\"", wraplength=300).pack(side='top', expand=True, anchor='nw')
        tk.Label(metadata, text="Duration: " + utils.convert_seconds_to_duration(youtube.length)) \
            .pack(side='top', expand=True, anchor='nw')
        tk.Label(metadata, text=str(utils.format_view_count(youtube.views)) + " Views")\
            .pack(side='top', expand=True, anchor='nw')
        tk.Label(metadata, text="Author: " + youtube.author).pack(side='top', expand=True, anchor='nw')

    # Creates a Tkinter PhotoImage from a thumbnail URL.
    def get_youtube_thumbnail(self, thumbnail_url):
        # Creates a local temp-file for the thumbnail.
        temp_file = urllib.request.urlretrieve(url=thumbnail_url)[0]

        # Access the thumbnail, resize it, and return as PhotoImage
        img = Image.open(fp=temp_file)
        img = img.resize((160, 90), Image.ANTIALIAS)

        # Thumbnail image is added to a list to retain reference to it. Otherwise, it will disappear after short time.
        thumbnail = ImageTk.PhotoImage(img)
        self.cached_thumbnails.append(thumbnail)

        # Erase any remaining temp files.
        urllib.request.urlcleanup()

        return thumbnail
