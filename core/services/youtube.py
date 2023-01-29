import time

from pytube import YouTube

from core.services import files


def get_YouTube_object(link):
    return YouTube(link)


def download_stream(console, youtube, itag):
    # May prompt the user for a save dir before downloading
    selected_loc = files.get_save_location()

    if selected_loc is None:
        console.printError('Could not download file. No save location was specified.')
        return

    console.printInfo('Downloading media now..')

    # Download the file
    start_time = time.time()
    filepath = youtube.streams.get_by_itag(itag).download(output_path=selected_loc)

    # print a success message
    console.printSuccess('Downloaded media as \"' + filepath + "\". (" +
                              str(round(time.time() - start_time, 2)) + "s)")
