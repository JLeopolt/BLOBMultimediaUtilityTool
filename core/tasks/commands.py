from core.gui.main import main_frame
from core.tasks import subcoms, Load as com_load
from core.utility import executor


# Resets the window.
def Clear():
    main_frame.clear()


# Executes the selected process.
def Run():
    Load_Async()


# async Loads the media from the URL.
def Load_Async():
    # Get the URL from user input field.
    url = main_frame.link_entry_field.get()
    # execute async
    executor.execute_process(com_load.run, url)


# Loads the media from the URL. Chainable.
# Returns True if successful, False otherwise.
def Load_Sync():
    # Get the URL from user input field.
    url = main_frame.link_entry_field.get()
    # Execute the Load command synchronously.
    return com_load.run(url)


# Loads -> Auto download Video at highest res.
def Video():
    # Asynchronously executes chain command.
    executor.execute_process(Chain, [(Load_Sync, None), (subcoms.auto_download_hr, 0)])


# Loads -> Auto download audio at highest res.
def Audio():
    # Asynchronously executes chain command.
    executor.execute_process(Chain, [(Load_Sync, None), (subcoms.auto_download_hr, 1)])


# Expects [(process, args), (subcommand, args)]
# args can be left as None if no arguments should be provided.
# This function call should be executed async.
def Chain(process_schedule):
    process = process_schedule[0]
    subcom = process_schedule[1]

    # Execute the main process
    process_success: bool
    if process[1] is not None:
        process_success = process[0](process[1])
    else:
        process_success = process[0]()

    # If the process return False, do not continue.
    if process_success is False:
        return

    # If the process was successful
    # execute the subcommand.
    if subcom[1] is not None:
        subcom[0](subcom[1])
    else:
        subcom[0]()
