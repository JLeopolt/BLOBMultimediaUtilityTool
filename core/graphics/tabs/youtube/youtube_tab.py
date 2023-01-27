from tkinter import ttk
import urllib
from urllib import request
from PIL import Image, ImageTk
from threading import Thread
import time
import core.services.youtube
from core.graphics.common.components import console

cached_thumbnails = []


# Creates a Tkinter PhotoImage from a thumbnail URL.
def get_youtube_thumbnail(thumbnail_url):
    # Creates a local temp-file for the thumbnail.
    temp_file = urllib.request.urlretrieve(url=thumbnail_url)[0]
    print("Thumbnail temporarily stored at " + temp_file)

    # Access the thumbnail, resize it, and return as PhotoImage
    img = Image.open(fp=temp_file)
    img = img.resize((160, 90), Image.ANTIALIAS)

    # Thumbnail image is added to a list to retain reference to it. Otherwise, it will disappear after short time.
    cached_thumbnails.append(img)
    return ImageTk.PhotoImage(img)


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


class YoutubeTab(ttk.Frame):
    # The notebook which maintains Download Options
    dl_options_nb = None

    # The tabs for the download options, 'Video' and 'Audio'
    video_download_option_tab = None
    audio_download_option_tab = None

    # Entry box for the YouTube link
    link_entry_field = None

    # Console for debugging
    console = None

    def __init__(self):
        super().__init__()

        # Prepare the YouTube tab.
        self.build()

    def build(self):
        # label
        label = ttk.Label(self, text='Enter YouTube URL:')
        label.grid(column=0, row=0, padx=10, pady=10, sticky='w')
        # entry
        self.link_entry_field = ttk.Entry(self)
        self.link_entry_field.grid(column=1, row=0, padx=10, pady=10, sticky='w')
        # button
        btn = ttk.Button(self, text='Load', command=self.schedule_youtube_video_access)
        btn.grid(column=2, row=0, padx=10, pady=10, sticky='w')

        # Tab label
        download_type_frame = ttk.LabelFrame(self, text='Download Type')
        download_type_frame.grid(column=0, columnspan=3, row=3, padx=10, pady=10, sticky='w')

        # Create Notebook and Tabs
        self.dl_options_nb = ttk.Notebook(download_type_frame)
        self.video_download_option_tab = ttk.Frame(self.dl_options_nb)
        self.audio_download_option_tab = ttk.Frame(self.dl_options_nb)

        # Set up the Notebook
        self.dl_options_nb.add(self.video_download_option_tab, text='Video')
        self.dl_options_nb.add(self.audio_download_option_tab, text='Audio')
        self.dl_options_nb.grid(padx=10, pady=10, sticky='w')

        # Add the console
        self.console = core.graphics.common.components.console.Console(self)
        self.console.grid(columnspan=4, row=4, padx=10, pady=10, sticky='s')

    def download_youtube_video(self):
        # Get the YouTube link from user input
        youtube_link = self.link_entry_field.get()
        if youtube_link == "":
            self.console.printError("No link was provided.")
            return

        progress_bar = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='indeterminate',
            length=500
        )
        progress_bar.grid(column=0, columnspan=4, row=2, padx=10, pady=10, sticky='we')
        progress_bar.start()

        start_time = time.time()

        # Get the stream from pytube after getting the link.
        youtube = core.services.youtube.get_YouTube_object(youtube_link)

        thumbnail_image = get_youtube_thumbnail(youtube.thumbnail_url)
        thumbnail = ttk.Label(self, image=thumbnail_image)
        thumbnail.grid(column=0, row=3, padx=10, pady=10, sticky='w')
        title = ttk.Label(self, text=youtube.title)
        title.grid(column=1, row=3, padx=10, pady=10, sticky='w')

        mid_time = time.time()
        self.console.printInfo("Accessed video metadata. (" + str(round(mid_time - start_time, 2))
                               + "s) Now retrieving download streams..")

        self.display_youtube_download_options(youtube)

        # Success message to notify the user
        self.console.printSuccess("Retrieved all available download streams for \"" + youtube.title + "\" ("
                                  + str(round(time.time() - mid_time, 2)) + "s).")

        # Stop progress bar, and remove it
        progress_bar.stop()
        progress_bar.grid_forget()

    def display_youtube_download_options(self, youtube):
        # Add all Video download options
        for source in youtube.streams.filter():
            # Where to add the option to
            tab_location = self.audio_download_option_tab
            # If both video & audio present, adds it to the Video tab.
            if source.includes_video_track:
                tab_location = self.video_download_option_tab

            # Generate the button representing this download option, and add it to the specified tab.
            rb = ttk.Button(
                tab_location,
                text=get_source_title(source)
            )
            # Add the button
            rb.pack(expand=True, fill='both')

    # Opens a thread which will update the Youtube download options list.
    def schedule_youtube_video_access(self):
        worker = Thread(target=self.download_youtube_video)
        worker.start()
