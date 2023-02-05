import tkinter as tk
import urllib
from tkinter import ttk
from urllib import request
from PIL import Image, ImageTk
from core.graphics.common import utils
from core.services import files


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

    def build_from_youtube(self, youtube):
        self.reset()

        # The thumbnail image
        thumbnail_image = self.create_thumbnail_from_url(youtube.thumbnail_url)
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

    # Creates a thumbnail from a URL.
    def create_thumbnail_from_url(self, thumbnail_url):
        # Creates a local temp-file for the thumbnail.
        temp_file = urllib.request.urlretrieve(url=thumbnail_url)[0]
        return self.create_thumbnail(temp_file)

    # Creates a thumbnail from a filepath
    def create_thumbnail(self, filepath):
        # Access the thumbnail, resize it, and return as PhotoImage
        img = Image.open(fp=filepath)
        img = img.resize((160, 90), Image.ANTIALIAS)

        # Thumbnail image is added to a list to retain reference to it. Otherwise, it will disappear after short time.
        thumbnail = ImageTk.PhotoImage(img)
        self.cached_thumbnails.append(thumbnail)

        # Erase any remaining temp files.
        urllib.request.urlcleanup()

        return thumbnail

    def build_from_file(self, url_meta):
        self.reset()

        # The thumbnail image
        thumbnail_image = self.create_thumbnail("core/assets/no-source.png")
        thumbnail = ttk.Label(self, image=thumbnail_image)
        thumbnail.pack(side='left', anchor='nw')

        # Video metadata frame
        metadata = tk.Frame(self)
        metadata.pack(side='left', anchor='nw')

        # Get all metadata from the file URL without downloading it.
        tk.Label(metadata, text="File: " + url_meta.filename).pack(side='top', expand=True, anchor='nw')
        tk.Label(metadata, text="Website: " + url_meta.domain).pack(side='top', expand=True, anchor='nw')
        tk.Label(metadata, text="Resolved DNS: " + url_meta.host_addr).pack(side='top', expand=True, anchor='nw')
