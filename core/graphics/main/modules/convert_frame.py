import tkinter as tk
from threading import Thread
from tkinter import ttk

from core.graphics.common import utils
from core.graphics.common.progressbar import ProgressBar
from core.graphics.main.modules.stream_selector import StreamSelector
from core.services import youtube as yt, direct_file as dir_f, blob


# The display frame which allows the user to select a download stream, convert file types, etc.
class ConvertFrame(ttk.LabelFrame):
    enable_stream_select = None
    # output mode
    output_mode = None
    # stream selector
    video_stream_selector = None
    audio_stream_selector = None
    # file conversion
    file_convert_type = None
    file_type_menu = None
    custom_file_convert_type = None

    # Upon construction the frame is empty and won't show up until build() is called.
    def __init__(self, container, console):
        super().__init__(container, text='Convert & Download')
        self.console = console
        # preset file types for videos
        self.preset_video_filetypes = ['.mp4', '.mov', '.wmv', '.avi', '.mkv', '.webm']
        # preset file types for audio
        self.preset_audio_filetypes = ['.mp3', '.wav', '.ogg', '.flac', '.aiff']

    def reset(self):
        utils.destroy_children(self)
        ttk.Frame(self, width=0, height=0, borderwidth=0).pack()

    # resets the frame and builds it again.
    def build_from_youtube(self, youtube):
        # reset frame
        self.reset()
        self.enable_stream_select = True

        # create and start the progress bar now.
        progress_bar = ProgressBar(self)
        progress_bar.pack(side='top', expand=True, fill='x', anchor='nw')
        progress_bar.start()

        # initially retrieve the Streams.
        # This call takes a long time, but after it's done, streams can be freely used.
        youtube.streams.filter(adaptive=True)
        progress_bar.stop()

        # build output mode frame.
        self.output_mode = tk.StringVar()
        output_mode_frame = self.build_output_mode_frame()
        output_mode_frame.pack(side='left', expand=True)

        # streams are selected in this section
        stream_select_frame = self.build_stream_select_frame(youtube)
        stream_select_frame.pack(side='left', expand=True)

        # the file conversion takes place here
        file_convert_frame = self.build_file_convert_frame(self.preset_video_filetypes)
        file_convert_frame.pack(side='left', expand=True)

        # the final request can be submitted in this section
        finish_frame = self.build_finish_frame(yt.download, youtube)
        finish_frame.pack(side='left', expand=True)

    # expects a FileURLMetadata object
    def build_from_file(self, url_meta):
        # reset frame
        self.reset()
        self.enable_stream_select = False

        # build output mode frame.
        self.output_mode = tk.StringVar()
        output_mode_frame = self.build_output_mode_frame()
        output_mode_frame.pack(side='left', expand=True)

        # download source is shown in this section
        source_select_frame = ttk.Frame(self)
        ttk.Label(source_select_frame, text='Download Streams').pack()
        ttk.Label(source_select_frame, text='File: '+url_meta.filename).pack()
        source_select_frame.pack(side='left', expand=True)

        # the file conversion takes place here
        file_convert_frame = self.build_file_convert_frame(self.preset_video_filetypes)
        file_convert_frame.pack(side='left', expand=True)

        # the final request can be submitted in this section
        finish_frame = self.build_finish_frame(dir_f.download, url_meta)
        finish_frame.pack(side='left', expand=True)

    # Selects which output mode to use. Changes which options show up in the converter tab when selected.
    def build_output_mode_frame(self):
        output_mode_selector_frame = ttk.Frame(self)
        ttk.Label(output_mode_selector_frame, text='Output Mode').pack()
        output_mode_selector = ttk.OptionMenu(output_mode_selector_frame,
                                              self.output_mode,
                                              'Video',
                                              *['Video', 'Audio', 'Mute Video'],
                                              command=self.update_output_mode)
        output_mode_selector.pack()
        return output_mode_selector_frame

    # Updates convert elements based on the output mode selected.
    # value is the value of the output_mode optionmenu, automatically passed into the command.
    def update_output_mode(self, value):
        if value == 'Video':
            self.set_video_mode()
        elif value == 'Audio':
            self.set_audio_mode()
        elif value == 'Mute Video':
            self.set_muted_vid_mode()

    # Updates the Converter Frame to 'Audio' output mode.
    def set_audio_mode(self):
        # Only use an audio stream.
        if self.enable_stream_select:
            self.video_stream_selector.configure(state='disabled')
            self.audio_stream_selector.configure(state='enabled')
        # file output as audio
        self.update_file_type_menu_options(self.preset_audio_filetypes)

    # Updates the Converter Frame to 'Video' output mode.
    def set_video_mode(self):
        # Use both a Video and Audio stream.
        if self.enable_stream_select:
            self.video_stream_selector.configure(state='enabled')
            self.audio_stream_selector.configure(state='enabled')
        # file output as video
        self.update_file_type_menu_options(self.preset_video_filetypes)

    # Updates the Converter Frame to 'Mute Video' output mode.
    def set_muted_vid_mode(self):
        # Use ONLY a video stream.
        if self.enable_stream_select:
            self.video_stream_selector.configure(state='enabled')
            self.audio_stream_selector.configure(state='disabled')
        # file output as video
        self.update_file_type_menu_options(self.preset_video_filetypes)

    # streams are selected in this section
    def build_stream_select_frame(self, youtube):
        stream_select_frame = ttk.Frame(self)
        ttk.Label(stream_select_frame, text='Download Streams').pack()

        # list of all video streams, in descending order of resolution
        videos = youtube.streams.filter(adaptive=True).order_by('resolution').__reversed__()
        self.video_stream_selector = StreamSelector(stream_select_frame, videos)
        self.video_stream_selector.pack()

        # list of all audio streams, in descending order of bit-rate
        audios = youtube.streams.filter(adaptive=True, only_audio=True).order_by('abr').__reversed__()
        self.audio_stream_selector = StreamSelector(stream_select_frame, audios)
        self.audio_stream_selector.pack()

        return stream_select_frame

    # the file conversion takes place here
    def build_file_convert_frame(self, file_type_presets):
        file_convert_frame = ttk.Frame(self)
        ttk.Label(file_convert_frame, text='Output File Type').pack(side='top')

        # Selector, the user can select from a preset list of possible file types.
        self.file_convert_type = tk.StringVar(file_convert_frame)
        self.file_type_menu = ttk.OptionMenu(file_convert_frame,
                                             self.file_convert_type,
                                             file_type_presets[0],
                                             *file_type_presets,
                                             command=self.reset_custom_type_entrybox)
        self.file_type_menu.pack(side='left')

        # entry box, the user can enter a custom file type.
        # ttk.Label(file_convert_frame, text='Custom File Type').pack()
        self.custom_file_convert_type = tk.StringVar(file_convert_frame)
        ttk.Entry(file_convert_frame, textvariable=self.custom_file_convert_type, width=6).pack(side='left')

        return file_convert_frame

    # updates the choices in the file type option menu
    def update_file_type_menu_options(self, file_type_presets):
        # delete old filetypes
        self.file_type_menu['menu'].delete(0, 'end')
        # add all new file types
        for filetype in file_type_presets:
            self.file_type_menu['menu'].add_command(label=filetype, command=tk._setit(self.file_convert_type, filetype))
        # set default value
        self.file_convert_type.set(file_type_presets[0])

    # if a preset file type is selected, reset custom file type entrybox.
    def reset_custom_type_entrybox(self, value):
        self.custom_file_convert_type.set('')
        self.file_type_menu.focus()

    # the final request can be submitted in this section
    def build_finish_frame(self, funct, data):
        finish_frame = ttk.Frame(self)
        ttk.Label(finish_frame, text='Finish').pack()

        ttk.Button(finish_frame, text='Download', command=lambda: self.async_download(funct, data)).pack()
        return finish_frame

    def async_download(self, funct, data):
        # execute on a new thread
        worker_thread = Thread(target=funct, args=[self, data])
        worker_thread.start()

    # returns the filename in form: <filename>.<extension>
    def get_output_filename(self, filename):
        # if there is no custom file type, use the selected preset
        if utils.trim(self.custom_file_convert_type.get()) is None or '':
            return filename + self.custom_file_convert_type.get()

        return filename + self.file_convert_type.get()
