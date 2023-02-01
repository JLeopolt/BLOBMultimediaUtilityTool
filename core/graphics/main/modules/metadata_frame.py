import urllib
from urllib import request
from tkinter import ttk
import tkinter as tk
from core.graphics.common import utils
from PIL import Image, ImageTk


class MetadataFrame(ttk.LabelFrame):

    # Cached thumbnails, maintain reference so they don't disappear
    cached_thumbnails = []

    def __init__(self, container):
        super().__init__(container, text='Metadata')

    def reset_cache(self):
        self.cached_thumbnails = []

    def reset(self):
        utils.destroy_children(self)
        ttk.Frame(self, width=0, height=0, borderwidth=0).pack()
        self.reset_cache()

    def build(self, youtube):
        self.reset()

        # The thumbnail image
        thumbnail_image = self.get_youtube_thumbnail(youtube.thumbnail_url)
        thumbnail = ttk.Label(self, image=thumbnail_image)
        thumbnail.pack(side='left', anchor='nw')

        # Video metadata
        metadata = tk.Frame(self)
        metadata.pack(side='left', anchor='nw')
        tk.Label(metadata, text="\"" + youtube.title + "\"").pack(side='top', expand=True, anchor='nw')
        tk.Label(metadata, text="Duration: " + utils.convert_seconds_to_duration(youtube.length)) \
            .pack(side='top', expand=True, anchor='nw')
        tk.Label(metadata, text=str(utils.format_view_count(youtube.views)) + " Views") \
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
