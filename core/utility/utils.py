from datetime import datetime


# Creates a descriptor title for a download stream.
def get_source_title(source):
    title = "."

    # Get the resolution for video, or bit-rate for audio.
    if source.type == 'video':
        title += source.mime_type.replace("video/", "") + " "
        title += source.resolution + " " + str(source.fps) + "fps"
    elif source.type == 'audio':
        title += source.mime_type.replace("audio/", "") + " "
        title += source.abr

    # Add the file size in parentheses
    title += " (" + str(round(source.filesize_mb, 2)) + " mb)"

    return title


# Converts a number of seconds into a timestamp of HH:MM:SS (HH is ignored unless > 0)
def convert_seconds_to_duration(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    duration = str(s)
    if s < 10:
        duration = "0" + duration
    if m > 0:
        duration = str(m) + ":" + duration
    if h > 0:
        if m < 10:
            duration = "0" + duration
        return str(h) + ":" + duration
    return duration


def format_view_count(views):
    return format(views, ',d')


# Destroys all children of a frame.
def destroy_children(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# Performs pack_forget for all children of a frame.
def pack_forget_children(frame):
    for widget in frame.winfo_children():
        widget.pack_forget()


# Removes all whitespace, tab, newline, etc. from a string and returns.
def trim(text):
    return text.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")


# Returns date time in M/D/Y H:M:S format.
def get_date_time():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")
