# The display frame which allows the user to select a download stream, convert file types, etc.

import tkinter as tk
from threading import Thread
from tkinter import ttk

from core.graphics.common import utils
from core.graphics.common.progressbar import ProgressBar
from core.graphics.main.modules.stream_selector import StreamSelector
from core.services import youtube as yt, direct_file as dir_f, files

# Note -- type-hints used to prevent warnings. These values are not initialized until build methods called.
widget: ttk.LabelFrame

enable_stream_select: bool

# output mode
output_mode: tk.StringVar

# stream selector
video_stream_selector: StreamSelector
audio_stream_selector: StreamSelector

# file conversion
file_convert_type: tk.StringVar
file_type_menu: ttk.OptionMenu
custom_file_convert_type: tk.StringVar


# Upon construction the frame is empty and won't show up until a specific build method is called.
def build(parent):
    global widget
    widget = ttk.LabelFrame(parent, text='Convert & Download')
    widget.pack(side='top', fill='x', anchor='n')


def reset():
    utils.destroy_children(widget)
    # add an invisible widget to the frame to keep the border rendered.
    ttk.Frame(widget, width=0, height=0, borderwidth=0).pack()


# resets the frame and builds it again, using a YouTube object as the source
def build_from_youtube(youtube):
    # reset frame
    reset()
    global enable_stream_select
    enable_stream_select = True

    # create and start a progress bar now.
    progress_bar = ProgressBar(widget)
    progress_bar.pack(side='top', expand=True, fill='x', anchor='nw')
    progress_bar.start()

    # initially retrieve the Streams.
    # This call takes a long time, but after it's done, streams can be freely used.
    youtube.streams.filter(adaptive=True)
    progress_bar.stop()

    # build output mode frame.
    global output_mode
    output_mode = tk.StringVar()
    output_mode_frame = build_output_mode_frame()
    output_mode_frame.pack(side='left', expand=True)

    # streams are selected in this section
    stream_select_frame = build_stream_select_frame(youtube)
    stream_select_frame.pack(side='left', expand=True)

    # the file conversion takes place here
    file_convert_frame = build_file_convert_frame(files.video_filetypes)
    file_convert_frame.pack(side='left', expand=True)

    # the final request can be submitted in this section
    finish_frame = build_finish_frame(yt.download, youtube)
    finish_frame.pack(side='left', expand=True)


# expects a FileURLMetadata object
def build_from_file(url_meta):
    # reset frame
    reset()
    global enable_stream_select
    enable_stream_select = False

    # build output mode frame.
    global output_mode
    output_mode = tk.StringVar()
    output_mode_frame = build_output_mode_frame()
    output_mode_frame.pack(side='left', expand=True)

    # download source is shown in this section
    source_select_frame = ttk.Frame(widget)
    ttk.Label(source_select_frame, text='Download Streams').pack()
    ttk.Label(source_select_frame, text='File: ' + url_meta.filename).pack()
    source_select_frame.pack(side='left', expand=True)

    # the file conversion takes place here
    file_convert_frame = build_file_convert_frame(files.video_filetypes)
    file_convert_frame.pack(side='left', expand=True)

    # the final request can be submitted in this section
    finish_frame = build_finish_frame(dir_f.download, url_meta)
    finish_frame.pack(side='left', expand=True)


# Selects which output mode to use. Changes which options show up in the converter tab when selected.
def build_output_mode_frame():
    output_mode_selector_frame = ttk.Frame(widget)
    ttk.Label(output_mode_selector_frame, text='Output Mode').pack()
    output_mode_selector = ttk.OptionMenu(output_mode_selector_frame,
                                          output_mode,
                                          'Video',
                                          *['Video', 'Audio', 'Mute Video'],
                                          command=update_output_mode)
    output_mode_selector.pack()
    return output_mode_selector_frame


# Updates convert elements based on the output mode selected.
# value is the value of the output_mode optionmenu, automatically passed into the command.
def update_output_mode(value):
    if value == 'Video':
        set_video_mode()
    elif value == 'Audio':
        set_audio_mode()
    elif value == 'Mute Video':
        set_muted_vid_mode()


# Updates the Converter Frame to 'Audio' output mode.
def set_audio_mode():
    # Only use an audio stream.
    if enable_stream_select:
        video_stream_selector.configure(state='disabled')
        audio_stream_selector.configure(state='enabled')
    # file output as audio
    update_file_type_menu_options(files.audio_filetypes)


# Updates the Converter Frame to 'Video' output mode.
def set_video_mode():
    # Use both a Video and Audio stream.
    if enable_stream_select:
        video_stream_selector.configure(state='enabled')
        audio_stream_selector.configure(state='enabled')
    # file output as video
    update_file_type_menu_options(files.video_filetypes)


# Updates the Converter Frame to 'Mute Video' output mode.
def set_muted_vid_mode():
    # Use ONLY a video stream.
    if enable_stream_select:
        video_stream_selector.configure(state='enabled')
        audio_stream_selector.configure(state='disabled')
    # file output as video
    update_file_type_menu_options(files.video_filetypes)


# streams are selected in this section
def build_stream_select_frame(youtube):
    stream_select_frame = ttk.Frame(widget)
    ttk.Label(stream_select_frame, text='Download Streams').pack()

    # list of all video streams, in descending order of resolution
    videos = youtube.streams.filter(adaptive=True).order_by('resolution').__reversed__()
    global video_stream_selector
    video_stream_selector = StreamSelector(stream_select_frame, videos)
    video_stream_selector.pack()

    # list of all audio streams, in descending order of bit-rate
    audios = youtube.streams.filter(adaptive=True, only_audio=True).order_by('abr').__reversed__()
    global audio_stream_selector
    audio_stream_selector = StreamSelector(stream_select_frame, audios)
    audio_stream_selector.pack()

    return stream_select_frame


# the file conversion takes place here
def build_file_convert_frame(file_type_presets):
    file_convert_frame = ttk.Frame(widget)
    ttk.Label(file_convert_frame, text='Output File Type').pack(side='top')

    # Selector, the user can select from a preset list of possible file types.
    global file_convert_type
    file_convert_type = tk.StringVar(file_convert_frame)
    global file_type_menu
    file_type_menu = ttk.OptionMenu(file_convert_frame,
                                    file_convert_type,
                                    file_type_presets[0],
                                    *file_type_presets,
                                    command=reset_custom_type_entrybox)
    file_type_menu.pack(side='left')

    # entry box, the user can enter a custom file type.
    # ttk.Label(file_convert_frame, text='Custom File Type').pack()
    global custom_file_convert_type
    custom_file_convert_type = tk.StringVar(file_convert_frame)
    ttk.Entry(file_convert_frame, textvariable=custom_file_convert_type, width=6).pack(side='left')

    return file_convert_frame


# updates the choices in the file type option menu
def update_file_type_menu_options(file_type_presets):
    # delete old filetypes
    file_type_menu['menu'].delete(0, 'end')
    # add all new file types
    for filetype in file_type_presets:
        file_type_menu['menu'].add_command(label=filetype, command=tk._setit(file_convert_type, filetype))
    # set default value
    file_convert_type.set(file_type_presets[0])


# if a preset file type is selected, reset custom file type entrybox.
def reset_custom_type_entrybox(value):
    custom_file_convert_type.set('')
    file_type_menu.focus()


# the final request can be submitted in this section
def build_finish_frame(funct, data):
    finish_frame = ttk.Frame(widget)
    ttk.Label(finish_frame, text='Finish').pack()

    ttk.Button(finish_frame, text='Download', command=lambda: async_download(funct, data)).pack()
    return finish_frame


def async_download(funct, data):
    # execute on a new thread
    worker_thread = Thread(target=funct, args=[data])
    worker_thread.start()


# returns the filename in form: <filename>.<extension>
def get_output_filename(filename):
    # if there is no custom file type, use the selected preset
    if utils.trim(custom_file_convert_type.get()) is None or '':
        return filename + custom_file_convert_type.get()

    return filename + file_convert_type.get()
