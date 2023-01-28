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
