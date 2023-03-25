# Tracks and manages asynchronous execution of processes.
# also manages downloads.

from core.gui.main.components import console, shortcut_panel
from threading import Thread


# the thread which will perform any async task, one at a time.
process_thread = None


# Checks if the worker thread is open. If busy, returns True and prints an error message.
def thread_busy():
    global process_thread
    if process_thread is not None and process_thread.is_alive():
        console.printError('Please wait for the current process to finish before scheduling a new process.')
        return True
    return False


# Asynchronously executes the provided process if possible.
# Automatically blocks and unblocks shortcut panel.
# If None is passed as args, no arguments are used.
def execute_process(process, args):
    # fails if the thread is busy.
    if thread_busy():
        return

    # perform the process on the worker thread
    global process_thread
    process_args = [process, args]
    if args is None:
        process_args = [process]
    process_thread = Thread(target=perform_process, args=process_args)
    process_thread.start()


# Wraps the process execution with shortcut blocking / unblocking.
# No matter whether process is successful or not, it will unblock once complete.
def perform_process(process, args):
    # Block new processes.
    shortcut_panel.block_new_processes()
    # execute the process
    process(args)
    # after process terminates, unblock processes.
    shortcut_panel.unblock_new_processes()


# Asynchronously performs a download. This is distinct from a process;
# since it doesn't use the shared worker thread.
def perform_download(download_funct, args):
    temp_thread = Thread(target=download_funct, args=[args])
    temp_thread.start()
