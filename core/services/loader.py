import time
from pytube.exceptions import RegexMatchError
import core
import core.services.youtube
import core.graphics.common.utils as utils
import requests
from core.services import files


# takes in the main frame. loads in the youtube video from link provided
# should be called asynchronously.
def load_youtube_video(main):
    # Get the YouTube link from user input
    youtube_link = main.link_entry_field.get()
    if utils.trim(youtube_link) == '':
        main.console.printError("No link was provided.")
        return

    main.short_cuts.block_new_processes()

    # Start the progress bar
    start_time = time.time()

    # Get the metadata here.
    try:
        youtube = core.services.youtube.get_YouTube_object(youtube_link)
    except RegexMatchError:
        main.console.printError("Input is not a valid URL.")
        main.short_cuts.unblock_new_processes()
        return
    except (Exception,) as e:
        main.console.printError(str(e))
        main.short_cuts.unblock_new_processes()
        return

    # resets, then builds the metadata frame
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


# takes in the main frame. loads in BLOB media from the link provided.
# should be called asynchronously.
def load_BLOB(main):
    x = 0


# takes in the main frame. loads a File from the link provided.
# should be called asynchronously.
def load_file_URL(main):
    # Get the file URL
    file_URL = main.link_entry_field.get()
    if utils.trim(file_URL) == '':
        main.console.printError("No URL was provided.")
        return

    # check if the URL is valid.
    try:
        head = requests.head(file_URL)
        if head.status_code != requests.codes.ok:
            raise Exception
    except (Exception,):
        main.console.printError("Input is not a valid URL.")
        return

    main.short_cuts.block_new_processes()

    # Start the progress bar
    start_time = time.time()

    # get metadata
    url_meta = files.FileURLMetadata(file_URL)

    # resets, then builds the metadata frame
    main.metadata_frame.build_from_file(url_meta)

    mid_time = time.time()
    main.console.printInfo("Got file metadata. (" + str(round(mid_time - start_time, 2)) + "s)")

    # Access the download streams here.
    # Readies the Converter frame.
    main.convert_frame.build_from_file(url_meta)

    # Success message to notify the user
    main.console.printSuccess("Retrieved all available download streams for " + file_URL + " ("
                              + str(round(time.time() - mid_time, 2)) + "s).")

    # Unblock shortcuts
    main.short_cuts.unblock_new_processes()
