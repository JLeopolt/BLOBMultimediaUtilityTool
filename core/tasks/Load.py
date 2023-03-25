import time

import requests
from pytube.exceptions import RegexMatchError

from core.gui.main.components import metadata_widget, convert_widget, console
from core.tasks.services import html, youtube
from core.utility import utils, files


# Processes the URL, determines which mode to process it with. takes in url as parameter.
# returns True if successful, false otherwise. May raise exception
def run(url):
    if utils.trim(url) == '':
        console.printError("Please provide a URL.")
        return False

    # convert url
    url = files.URLMetadata(url)

    if url.isYoutube:
        # Treat the URL as a YouTube link.
        return load_youtube_video(url_meta=url)

    # Open the URL and scan it's HTML Contents to find media files
    return load_scan(url_meta=url)


# Async, loads in the youtube video from link provided.
# Returns True if successful, false otherwise. May raise exceptions
def load_youtube_video(url_meta):
    start_time = time.time()

    # Get the metadata here.
    try:
        youtube_obj = youtube.get_YouTube_object(url_meta.url)
    except RegexMatchError:
        console.printError("Invalid YouTube URL.")
        return False

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
    return True


# Async, loads a File from the link provided.
# Returns True if successful, False otherwise.
def load_scan(url_meta):
    # check if the URL is valid.
    try:
        head = requests.head(url_meta.url)
        if head.status_code != requests.codes.ok:
            raise Exception
    except (Exception,):
        console.printError("Could not access URL. Ensure the URL is still active, then try again.")
        return False

    # Start the progress bar
    start_time = time.time()

    scanner = html.HTMLScanner(url_meta)
    vid_url = scanner.find_video()
    if vid_url is None:
        console.printError('Could not find an .mp4 video file at that URL.')
        return False
    video_url_meta = files.URLMetadata(vid_url)

    # resets, then builds the metadata frame
    metadata_widget.build_from_url(video_url_meta)

    # Readies the Converter frame.
    convert_widget.build_from_file(video_url_meta)

    console.printSuccess("Got file metadata. (" + str(round(time.time() - start_time, 2)) + "s)")
    return True
