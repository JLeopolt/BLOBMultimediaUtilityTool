import time
import tkinter as tk
import urllib
from idlelib.tooltip import Hovertip
from threading import Thread
from tkinter import ttk
from urllib import request
from PIL import Image, ImageTk
from pytube.exceptions import RegexMatchError
import core.services.youtube
from core.graphics.tabs.youtube.util import utils
from core.graphics.tabs.youtube import scontrols as shortcuts
from core.graphics.common import console as cs
from core.services import files


class YoutubeTab(ttk.Frame):
    # Entry box for the YouTube link
    link_entry_field = None

    # the output frame
    output_frame = None

    # The frame which contains the currently selected YouTube video's metadata
    youtube_metadata_frame = None

    # The tabs for the download options, 'Video' and 'Audio'
    video_download_option_tab = None
    audio_download_option_tab = None

    progress_bar = None

    # Console for debugging
    console = None

    # Cached thumbnails, maintain reference so they don't disappear
    cached_thumbnails = []

    def __init__(self):
        super().__init__()

        # Prepare the input frame
        input_frame = self.build_input_frame()
        input_frame.pack(side='top', fill='x', anchor='n')

        # Prepare the output frame
        self.output_frame = self.build_output_frame()
        self.output_frame.pack(side='top', fill='x', anchor='n')

        # Build the console
        console_frame = self.build_console()
        console_frame.pack(side='bottom', expand=True, fill='both')

    # returns all the input controls in a single Frame.
    def build_input_frame(self):
        # Instantiate the full frame
        input_frame = ttk.LabelFrame(self, text='Input')

        rich_control_frame = shortcuts.Shortcuts(input_frame, self.console)
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
    def build_output_frame(self):
        output_frame = ttk.LabelFrame(self, text='Output')

        self.progress_bar = ttk.Progressbar(
            output_frame,
            orient='horizontal',
            mode='indeterminate'
        )
        self.progress_bar.pack(side='top', expand=True, fill='x', anchor='nw')
        self.progress_bar.start()

        # Metadata frame
        self.youtube_metadata_frame = ttk.LabelFrame(output_frame, text='Metadata')
        self.youtube_metadata_frame.pack(side='left', expand=True, fill='both', anchor='nw')

        # Download Options frame
        download_type_frame = ttk.LabelFrame(output_frame, text='Download Type')
        download_type_frame.pack(side='right', fill='x')

        # Create Notebook and Tabs for Download Options
        dl_options_nb = ttk.Notebook(download_type_frame)
        self.video_download_option_tab = ttk.Frame(dl_options_nb)
        tk.Scrollbar(self.video_download_option_tab, orient="vertical").pack(side='right', fill='y')
        self.audio_download_option_tab = ttk.Frame(dl_options_nb)
        tk.Scrollbar(self.audio_download_option_tab, orient="vertical").pack(side='right', fill='y')

        # Set up the Notebook for Download Options
        dl_options_nb.add(self.video_download_option_tab, text='Video')
        dl_options_nb.add(self.audio_download_option_tab, text='Audio')
        dl_options_nb.pack()

        return output_frame

    def reset_output_frame(self):
        self.youtube_metadata_frame.pack_forget()
        self.output_frame = self.build_output_frame()

    # Opens a thread which will update the Youtube download options list.
    def schedule_youtube_video_access(self):
        worker = Thread(target=self.load_youtube_video)
        worker.start()

    # Returns a frame with the console.
    def build_console(self):
        # Instantiate the frame
        console_frame = ttk.LabelFrame(self, text='Console')

        self.console = cs.Console(console_frame)
        self.console.pack(side='bottom', expand=True, fill='both')

        return console_frame

    def load_youtube_video(self):
        # Get the YouTube link from user input
        youtube_link = self.link_entry_field.get()
        if youtube_link == "":
            self.console.printError("No link was provided.")
            return

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

        self.display_youtube_download_options(youtube)

        # Success message to notify the user
        self.console.printSuccess("Retrieved all available download streams for \"" + youtube.title + "\" ("
                                  + str(round(time.time() - mid_time, 2)) + "s).")

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
        tk.Label(metadata, text=str(youtube.views) + " Views").pack(side='top', expand=True, anchor='nw')
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

    def display_youtube_download_options(self, youtube):
        # Add all Video download options, sorted by Resolution
        for source in youtube.streams.filter().order_by('resolution').__reversed__():
            # Generate the button representing this download option, and add it to the video tab.
            rb = ttk.Button(
                self.video_download_option_tab,
                text=utils.get_source_title(source),
                command=lambda t=source.itag: self.download_stream(youtube, t),
            )
            # Add the button
            rb.pack(expand=True, fill='both')

        # Add all Audio download options, sorted by bit-rate.
        for source in youtube.streams.filter(only_audio=True).order_by('abr').__reversed__():
            # Generate the button representing this download option, and add it to the audio tab.
            rb = ttk.Button(
                self.audio_download_option_tab,
                text=utils.get_source_title(source),
                command=lambda t=source.itag: self.download_stream(youtube, t),
            )
            # Add the button
            rb.pack(expand=True, fill='both')

    def download_stream(self, youtube, itag):
        # May prompt the user for a save dir before downloading
        selected_loc = files.get_save_location()

        if selected_loc is None:
            self.console.printError('Could not download file. No save location was specified.')

        self.console.printInfo('Downloading media now..')

        # Download the file
        start_time = time.time()
        filepath = youtube.streams.get_by_itag(itag).download(output_path=selected_loc)

        # print a success message
        self.console.printSuccess('Downloaded media as \"' + filepath + "\". (" +
                                  str(round(time.time() - start_time, 2)) + "s)")
