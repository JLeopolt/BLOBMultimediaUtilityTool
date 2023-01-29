from tkinter import ttk, StringVar
from tkinter.ttk import OptionMenu
from core.services import youtube as yt
from core.graphics.common import utils


class MoreDownloadOptions(ttk.LabelFrame):

    def __init__(self, container, console):
        super().__init__(container, text='More Download Options')

        # Create Notebook and Tabs for Download Options
        dl_options_nb = ttk.Notebook(self)
        dl_options_nb.pack()

        # create tabs within the notebook for vid/audio
        self.video_frame = ttk.Frame(dl_options_nb)
        dl_options_nb.add(self.video_frame, text='Video')

        self.audio_frame = ttk.Frame(dl_options_nb)
        dl_options_nb.add(self.audio_frame, text='Audio')

        self.console = console

        self.youtube = None
        self.video_map = None
        self.audio_map = None

    def clear_options(self):
        # Destroy contents of Video, Audio tabs.
        utils.destroy_children(self.video_frame)
        utils.destroy_children(self.audio_frame)

    def show_options(self, youtube):
        self.youtube = youtube

        # list of all video streams, in descending order of resolution
        videos = youtube.streams.filter().order_by('resolution').__reversed__()
        # map the Title of the stream to it's itag
        self.video_map = {utils.get_source_title(source): source.itag for source in videos}

        temp_vid_option = StringVar(self.video_frame)
        temp_vid_option.set('More Video Options')

        video_options = OptionMenu(self.video_frame,
                                   temp_vid_option,
                                   *self.video_map.keys(),
                                   command=self.select_video_stream)
        video_options.pack()

        # list of all audio streams, in descending order of bit-rate
        audios = youtube.streams.filter(only_audio=True).order_by('abr').__reversed__()
        # map the Title of the stream to it's itag
        self.audio_map = {utils.get_source_title(source): source.itag for source in audios}

        temp_audio_opt = StringVar(self.audio_frame)
        temp_audio_opt.set('More Audio Options')

        audio_options = OptionMenu(self.audio_frame,
                                   temp_audio_opt,
                                   *self.audio_map.keys(),
                                   command=self.select_audio_stream)
        audio_options.pack()

    # Value is the name of the option selected, which is automatically passed in.
    def select_video_stream(self, value):
        itag = self.video_map.get(value)
        yt.download_stream(youtube=self.youtube, itag=itag, console=self.console)

    # Value is the name of the option selected, which is automatically passed in.
    def select_audio_stream(self, value):
        itag = self.audio_map.get(value)
        yt.download_stream(youtube=self.youtube, itag=itag, console=self.console)
