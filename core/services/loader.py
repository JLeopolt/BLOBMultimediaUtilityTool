import time
from pytube.exceptions import RegexMatchError
import requests

import core
from core.services import files, html, youtube
from core.graphics.common import utils, console
from core.graphics.main import shortcut_panel
from core.graphics.main import main_frame
from core.graphics.main.modules import metadata_widget, convert_widget


# Processes the URL to determine which mode to process it with.
def load():
    # Block new processes.
    shortcut_panel.block_new_processes()

    # Get the URL from user input field.
    url = main_frame.link_entry_field.get()
    if utils.trim(url) == '':
        console.printError("Please provide a URL.")
        shortcut_panel.unblock_new_processes()
        return

    url = files.URLMetadata(url)

    if url.isYoutube:
        # Treat the URL as a YouTube link.
        load_youtube_video(url_meta=url)
        return

    # Open the URL and scan it's HTML Contents to find media files
    load_scan(url_meta=url)


# loads in the youtube video from link provided
# should be called asynchronously.
def load_youtube_video(url_meta):
    start_time = time.time()

    # Get the metadata here.
    try:
        youtube_obj = core.services.youtube.get_YouTube_object(url_meta.url)
    except RegexMatchError:
        console.printError("Invalid YouTube URL.")
        shortcut_panel.unblock_new_processes()
        return
    except (Exception,) as e:
        console.printError(str(e))
        shortcut_panel.unblock_new_processes()
        return

    # builds the metadata frame
    metadata_widget.build_from_youtube(youtube_obj)
    mid_time = time.time()

    console.printInfo("Accessed video metadata. (" + str(round(mid_time - start_time, 2)) + "s)")
    console.printInfo("Retrieving download streams..")

    # Access the download streams here.
    # Readies the Converter frame.
    convert_widget.build_from_youtube(youtube=youtube_obj)

    # Success message to notify the user
    console.printSuccess("Retrieved all available download streams for \"" + youtube_obj.title + "\" ("
                         + str(round(time.time() - mid_time, 2)) + "s).")

    # Unblock shortcuts
    shortcut_panel.unblock_new_processes()


# loads a File from the link provided.
# should be called asynchronously.
def load_scan(url_meta):
    # check if the URL is valid.
    try:
        head = requests.head(url_meta.url)
        if head.status_code != requests.codes.ok:
            raise Exception
    except (Exception,):
        console.printError("Could not access URL. Ensure the URL is still active, then try again.")
        shortcut_panel.unblock_new_processes()
        return

    # Start the progress bar
    start_time = time.time()

    scanner = html.HTMLScanner(url_meta)
    vid_url = scanner.find_video()
    if vid_url is None:
        console.printError('Could not find an .mp4 video file at that URL.')
        shortcut_panel.unblock_new_processes()
        return
    video_url_meta = files.URLMetadata(vid_url)

    # resets, then builds the metadata frame
    metadata_widget.build_from_url(video_url_meta)

    # Readies the Converter frame.
    convert_widget.build_from_file(video_url_meta)

    # Unblock shortcuts
    shortcut_panel.unblock_new_processes()

    console.printSuccess("Got file metadata. (" + str(round(time.time() - start_time, 2)) + "s)")
