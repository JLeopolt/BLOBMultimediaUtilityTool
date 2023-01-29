from tkinter import filedialog

from core.graphics.common import utils

default_save_directory = "/"
prompt_for_downloads = True


# Returns true if the file dialog was cancelled or failed.
def was_cancelled(filepath):
    return utils.trim(filepath) == ''


# Asks the user to update their default save directory. Requires console to print a success message.
# Returns nothing.
def prompt_update_default_save_directory(console):
    global default_save_directory

    new_dir = filedialog.askdirectory(initialdir=default_save_directory, title='Update Default Save Location')
    if was_cancelled(new_dir):
        console.printError('Cancelled *SaveDir update, *SaveDir will remain \"'+default_save_directory+"\"")
        return

    default_save_directory = new_dir
    console.printInfo('Updated default save directory to: \"' + default_save_directory + "\".")


# Returns the directory to save to. If prompt is enabled, it will prompt user for a save location.
# Returns None if unsuccessful.
def get_save_location():
    # If user asked to be prompted before all downloads, prompt them for the save dir
    if prompt_for_downloads:
        loc = filedialog.askdirectory(initialdir=default_save_directory, title='Select A Save Location')
        if was_cancelled(loc):
            return None
        return loc
    # If auto download enabled, just download to the configured default dir.
    return default_save_directory
