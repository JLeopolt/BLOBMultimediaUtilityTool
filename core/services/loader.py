import time
from pytube.exceptions import RegexMatchError
import core
import core.services.youtube
import core.graphics.common.utils as utils
import requests
from core.services import files, blob


# Processes the URL to determine which mode to process it with.
def load(main):
    # Block new processes.
    main.short_cuts.block_new_processes()

    # Get the URL from user input field.
    url = main.link_entry_field.get()
    if utils.trim(url) == '':
        main.console.printError("Please provide a URL.")
        main.short_cuts.unblock_new_processes()
        return

    url = files.URLMetadata(url)

    if url.isYoutube:
        # Treat the URL as a YouTube link.
        load_youtube_video(main, url_meta=url)
        return
    # Scan the URL
    load_scan(main, url_meta=url)


# takes in the main frame. loads in the youtube video from link provided
# should be called asynchronously.
def load_youtube_video(main, url_meta):
    start_time = time.time()

    # Get the metadata here.
    try:
        youtube = core.services.youtube.get_YouTube_object(url_meta.url)
    except RegexMatchError:
        main.console.printError("Invalid YouTube URL.")
        main.short_cuts.unblock_new_processes()
        return
    except (Exception,) as e:
        main.console.printError(str(e))
        main.short_cuts.unblock_new_processes()
        return

    # builds the metadata frame
    main.metadata_frame.build_from_youtube(youtube)
    mid_time = time.time()

    main.console.printInfo("Accessed video metadata. (" + str(round(mid_time - start_time, 2)) + "s)")
    main.console.printInfo("Retrieving download streams..")

    # Access the download streams here.
    # Readies the Converter frame.
    main.convert_frame.build_from_youtube(youtube=youtube)

    # Success message to notify the user
    main.console.printSuccess("Retrieved all available download streams for \"" + youtube.title + "\" ("
                              + str(round(time.time() - mid_time, 2)) + "s).")

    # Unblock shortcuts
    main.short_cuts.unblock_new_processes()


# takes in the main frame. loads a File from the link provided.
# should be called asynchronously.
def load_scan(main, url_meta):
    # check if the URL is valid.
    try:
        head = requests.head(url_meta.url)
        if head.status_code != requests.codes.ok:
            raise Exception
    except (Exception,):
        main.console.printError("Could not access URL. Ensure the URL is still active, then try again.")
        main.short_cuts.unblock_new_processes()
        return

    # Start the progress bar
    start_time = time.time()

    scanner = blob.HTMLScanner(url_meta)
    vid_url = scanner.find_video()
    if vid_url is None:
        main.console.printError('Could not find an .mp4 video file at that URL.')
        main.short_cuts.unblock_new_processes()
        return
    video_url_meta = files.URLMetadata(vid_url)

    # resets, then builds the metadata frame
    main.metadata_frame.build_from_url(video_url_meta)

    # Readies the Converter frame.
    main.convert_frame.build_from_file(video_url_meta)

    # Unblock shortcuts
    main.short_cuts.unblock_new_processes()

    main.console.printSuccess("Got file metadata. (" + str(round(time.time() - start_time, 2)) + "s)")
