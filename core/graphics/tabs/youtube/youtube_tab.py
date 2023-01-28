import time
import urllib
from idlelib.tooltip import Hovertip
from threading import Thread
from tkinter import ttk, font
from urllib import request
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.scrolledtext as scrolledtext

import core.services.youtube
from core.graphics.common import console as cs


# Creates a descriptor title for a download stream.
def get_source_title(source):
    title = "."

    # Get the resolution for video, or bit-rate for audio.
    if source.type == 'video':
        title += source.mime_type.replace("video/", "") + " "
        title += source.resolution + " " + str(source.fps) + "fps"
    elif source.type == 'audio':
        title += source.mime_type.replace("audio/", "") + " "
        title += source.abr

    # Add the file size in parentheses
    title += " (" + str(round(source.filesize_mb, 2)) + " mb)"

    return title


# Converts a number of seconds into a timestamp of HH:MM:SS (HH is ignored unless > 0)
def convert_seconds_to_duration(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    duration = str(m) + ":" + str(s)
    if h > 0:
        return str(h) + ":" + duration
    return duration


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

        rich_control_frame = self.build_rich_controls_panel(input_frame)
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

    @staticmethod
    def build_rich_controls_panel(input_frame):
        # Robust controls panel
        special_control_frame = ttk.Frame(input_frame)

        run_button = ttk.Button(special_control_frame, text='\u25B6', width=3)
        run_button.pack(side='left', padx=1)
        Hovertip(run_button, '@Run: Executes the current script.')

        stop_button = ttk.Button(special_control_frame, text='\u25A0', width=3)
        stop_button.pack(side='left', padx=1)
        Hovertip(stop_button, '@Stop: Terminates current process.')

        clear_button = ttk.Button(special_control_frame, text='\u274C', width=3)
        clear_button.pack(side='left', padx=1)
        Hovertip(clear_button, '@Clear: Performs @Stop, then\nclears Output frame.')

        # Separator
        ttk.Separator(special_control_frame, orient='vertical').pack(side='left', padx=8, fill='y')

        audio_hr_button = ttk.Button(special_control_frame, text='\u266B', width=3)
        audio_hr_button.pack(side='left', padx=1)
        Hovertip(audio_hr_button, '@Audio.HR: Automatically downloads\naudio-only at highest resolution.')

        video_hr_button = ttk.Button(special_control_frame, text='\u2B73', width=3)
        video_hr_button.pack(side='left', padx=1)
        Hovertip(video_hr_button, '@Video.HR: Automatically downloads\nvideo w/ audio at highest resolution.')

        return special_control_frame

    # Returns the placeholder frame where YouTube video metadata and download options are shown.
    def build_output_frame(self):
        output_frame = ttk.LabelFrame(self, text='Output')

        # Metadata frame
        self.youtube_metadata_frame = ttk.LabelFrame(output_frame, text='Metadata')
        self.youtube_metadata_frame.pack(side='left', expand=True, fill='both', anchor='nw')

        # Download Options frame
        download_type_frame = ttk.LabelFrame(output_frame, text='Download Type')
        download_type_frame.pack(side='right', fill='both')
        # Create Notebook and Tabs for Download Options
        dl_options_nb = ttk.Notebook(download_type_frame)
        self.video_download_option_tab = ttk.Frame(dl_options_nb)
        self.audio_download_option_tab = ttk.Frame(dl_options_nb)
        # Set up the Notebook for Download Options
        dl_options_nb.add(self.video_download_option_tab, text='Video')
        dl_options_nb.add(self.audio_download_option_tab, text='Audio')
        dl_options_nb.pack()

        return output_frame

    def reset_output_frame(self):
        self.youtube_metadata_frame.pack_forget()
        self.output_frame = self.build_output_frame()

    # Returns a frame with the console.
    def build_console(self):
        # Instantiate the frame
        console_frame = ttk.LabelFrame(self, text='Console')

        self.console = cs.Console(console_frame)
        self.console.pack(side='bottom', expand=True, fill='both')

        return console_frame

    def download_youtube_video(self):
        # Get the YouTube link from user input
        youtube_link = self.link_entry_field.get()
        if youtube_link == "":
            self.console.printError("No link was provided.")
            return

        # progress_bar = ttk.Progressbar(
        #     self,
        #     orient='horizontal',
        #     mode='indeterminate',
        #     length=500
        # )
        # progress_bar.pack()
        # progress_bar.start()

        start_time = time.time()

        # Get the stream from pytube after getting the link.
        youtube = core.services.youtube.get_YouTube_object(youtube_link)

        self.update_youtube_metadata_frame(youtube)

        mid_time = time.time()
        self.console.printInfo("Accessed video metadata. (" + str(round(mid_time - start_time, 2)) + "s)")
        self.console.printInfo("Retrieving download streams..")

        self.display_youtube_download_options(youtube)

        # Success message to notify the user
        self.console.printSuccess("Retrieved all available download streams for \"" + youtube.title + "\" ("
                                  + str(round(time.time() - mid_time, 2)) + "s).")

        # Stop progress bar, and remove it
        # progress_bar.stop()

    # Updates the YouTube metadata frame with video's thumbnail, title, and duration.
    def update_youtube_metadata_frame(self, youtube):
        # The thumbnail image
        thumbnail_image = self.get_youtube_thumbnail(youtube.thumbnail_url)
        thumbnail = ttk.Label(self.youtube_metadata_frame, image=thumbnail_image)
        thumbnail.pack(side='left', anchor='nw')

        # Video metadata
        metadata = tk.Frame(self.youtube_metadata_frame)
        metadata.pack(side='left', anchor='nw')
        tk.Label(metadata, text="\"" + youtube.title + "\"").pack(side='top', expand=True, anchor='nw')
        tk.Label(metadata, text="Duration: " + convert_seconds_to_duration(youtube.length))\
            .pack(side='top', expand=True, anchor='nw')
        tk.Label(metadata, text=str(youtube.views) + " Views").pack(side='top', expand=True, anchor='nw')
        tk.Label(metadata, text="Author: " + youtube.author).pack(side='top', expand=True, anchor='nw')

    def display_youtube_download_options(self, youtube):
        # Add all Video download options, sorted by Resolution
        for source in youtube.streams.filter().order_by('resolution').__reversed__():
            # Generate the button representing this download option, and add it to the video tab.
            rb = ttk.Button(
                self.video_download_option_tab,
                text=get_source_title(source)
            )
            # Add the button
            rb.pack(expand=True, fill='both')

        # Add all Audio download options, sorted by bit-rate.
        for source in youtube.streams.filter(only_audio=True).order_by('abr').__reversed__():
            # Generate the button representing this download option, and add it to the audio tab.
            rb = ttk.Button(
                self.audio_download_option_tab,
                text=get_source_title(source)
            )
            # Add the button
            rb.pack(expand=True, fill='both')

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

    # Opens a thread which will update the Youtube download options list.
    def schedule_youtube_video_access(self):
        worker = Thread(target=self.download_youtube_video)
        worker.start()
