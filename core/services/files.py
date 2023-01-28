from tkinter import filedialog

default_save_directory = "/"
prompt_for_downloads = True


# Asks the user to update their default save directory. Requires console to print a success message.
def prompt_update_default_save_directory(console):
    global default_save_directory

    new_dir = filedialog.askdirectory(initialdir=default_save_directory)
    if new_dir is None:
        console.printInfo('Cancelled *SaveDir update.')
        return

    default_save_directory = new_dir
    console.printInfo('Updated default save directory to: \"' + default_save_directory + "\".")


# Returns the directory to save to. If prompt is enabled, it will prompt user for a save location.
def get_save_location():
    # If user asked to be prompted before all downloads, prompt them for the save dir
    if prompt_for_downloads:
        return filedialog.askdirectory(initialdir=default_save_directory)
    # If auto download enabled, just download to the configured default dir.
    return default_save_directory
