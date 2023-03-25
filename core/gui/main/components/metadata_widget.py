import tkinter as tk
import urllib
from tkinter import ttk
from urllib import request

from PIL import Image, ImageTk

from core.utility import utils, files

# The metadata frame widget
widget: ttk.LabelFrame

# Cached thumbnails, maintain reference so they don't disappear
cached_thumbnails = []


# Creates the metadata frame. Takes in the parent.
def build(parent):
    global widget
    widget = ttk.LabelFrame(parent, text='Metadata')
    widget.pack(side='top', fill='x', anchor='n')


# resets cached thumbnails
def reset_cache():
    global cached_thumbnails
    cached_thumbnails = []


# Resets the entire widget.
def reset():
    utils.destroy_children(widget)
    # An invisible widget is added to keep the border of the frame.
    ttk.Frame(widget, width=0, height=0, borderwidth=0).pack()
    reset_cache()


def build_from_youtube(youtube):
    reset()

    # The thumbnail image
    thumbnail_image = create_thumbnail_from_url(youtube.thumbnail_url)
    thumbnail = ttk.Label(widget, image=thumbnail_image)
    thumbnail.pack(side='left', anchor='nw')

    # Video metadata
    metadata = tk.Frame(widget)
    metadata.pack(side='left', anchor='nw')
    tk.Label(metadata, text="\"" + youtube.title + "\"").pack(side='top', expand=True, anchor='nw')
    tk.Label(metadata, text="Duration: " + utils.convert_seconds_to_duration(youtube.length)) \
        .pack(side='top', expand=True, anchor='nw')
    tk.Label(metadata, text=str(utils.format_view_count(youtube.views)) + " Views") \
        .pack(side='top', expand=True, anchor='nw')
    tk.Label(metadata, text="Author: " + youtube.author).pack(side='top', expand=True, anchor='nw')


def build_from_url(url_meta):
    reset()

    # The thumbnail image
    thumbnail_image = create_thumbnail(files.asset_path("no-source.png"))
    thumbnail = ttk.Label(widget, image=thumbnail_image)
    thumbnail.pack(side='left', anchor='nw')

    # Video metadata frame
    metadata = tk.Frame(widget)
    metadata.pack(side='left', anchor='nw')

    # Get all metadata from the file URL without downloading it.
    video_title_label = tk.Label(metadata, text="Filename: " + url_meta.filename)
    video_title_label.pack(side='top', expand=True, anchor='nw')
    tk.Label(metadata, text="Website: " + url_meta.domain).pack(side='top', expand=True, anchor='nw')
    tk.Label(metadata, text="Resolved DNS: " + url_meta.host_addr).pack(side='top', expand=True, anchor='nw')


# Creates a thumbnail from a URL.
def create_thumbnail_from_url(thumbnail_url):
    # Creates a local temp-file for the thumbnail.
    temp_file = urllib.request.urlretrieve(url=thumbnail_url)[0]
    return create_thumbnail(temp_file)


# Creates a thumbnail from a filepath
def create_thumbnail(filepath):
    # Access the thumbnail, resize it, and return as PhotoImage
    img = Image.open(fp=filepath)
    img = img.resize((160, 90), Image.ANTIALIAS)

    # Thumbnail image is added to a list to retain reference to it. Otherwise, it will disappear after short time.
    thumbnail = ImageTk.PhotoImage(img)
    cached_thumbnails.append(thumbnail)

    # Erase any remaining temp files.
    urllib.request.urlcleanup()

    return thumbnail