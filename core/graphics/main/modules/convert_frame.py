import tkinter as tk
from tkinter import ttk
from tkinter.ttk import OptionMenu

from core.graphics.common import utils
from core.graphics.common.progressbar import ProgressBar
from core.graphics.main.modules.stream_selector import StreamSelector


# The display frame which allows the user to select a download stream, convert file types, etc.
class ConvertFrame(ttk.LabelFrame):
    selected_mode = None
    video_stream_selector = None
    audio_stream_selector = None

    # Upon construction the frame is empty and won't show up until build() is called.
    def __init__(self, container):
        super().__init__(container, text='Convert & Download')

    def reset(self):
        utils.destroy_children(self)
        ttk.Frame(self, width=0, height=0, borderwidth=0).pack()

    # resets the frame and builds it again.
    def build(self, youtube):
        # reset frame
        self.reset()

        # create and start the progress bar now.
        progress_bar = ProgressBar(self)
        progress_bar.pack(side='top', expand=True, fill='x', anchor='nw')
        progress_bar.start()

        # initially retrieve the Streams.
        # This call takes a long time, but after it's done, streams can be freely used.
        youtube.streams.filter(adaptive=True)
        progress_bar.stop()

        # Selects which output mode to use. Changes which options show up in the converter tab when selected.
        self.selected_mode = tk.StringVar()
        output_mode_selector = OptionMenu(self, self.selected_mode,
                                          'Video',
                                          *['Video', 'Audio', 'Mute Video'],
                                          command=self.update_output_mode)
        output_mode_selector.pack()

        # list of all video streams, in descending order of resolution
        videos = youtube.streams.filter(adaptive=True).order_by('resolution').__reversed__()
        self.video_stream_selector = StreamSelector(self, videos)
        self.video_stream_selector.pack()

        # list of all audio streams, in descending order of bit-rate
        audios = youtube.streams.filter(adaptive=True, only_audio=True).order_by('abr').__reversed__()
        self.audio_stream_selector = StreamSelector(self, audios)
        self.audio_stream_selector.pack()

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
        self.video_stream_selector.configure(state='disabled')
        self.audio_stream_selector.configure(state='enabled')

    # Updates the Converter Frame to 'Video' output mode.
    def set_video_mode(self):
        # Use both a Video and Audio stream.
        self.video_stream_selector.configure(state='enabled')
        self.audio_stream_selector.configure(state='enabled')

    # Updates the Converter Frame to 'Mute Video' output mode.
    def set_muted_vid_mode(self):
        # Use ONLY a video stream.
        self.video_stream_selector.configure(state='enabled')
        self.audio_stream_selector.configure(state='disabled')
