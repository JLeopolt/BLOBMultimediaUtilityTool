from tkinter import ttk, StringVar

from core.graphics.common import utils


# An optionmenu which maintains a list of Streams behind-the-scenes.
# Useful for users to select from a sequence of streams, and return their selection.
class StreamSelector(ttk.OptionMenu):

    # The first element is the default selection.
    def __init__(self, container, streams):
        # set variables
        self.selection = StringVar(container)
        self.streams = streams

        # create a map of the Title of the stream to it's itag
        self.stream_map = {utils.get_source_title(source): source.itag for source in streams}

        # build the menu, each opt is the stream's 'title' , when selected it is resolved to an itag.
        super().__init__(container, self.selection, list(self.stream_map.keys())[0], *self.stream_map.keys())

    # Returns the currently selected option, as stream itag.
    # if a selection hasn't been made (Set to default string) returns None.
    def get_selected_itag(self):
        return self.stream_map.get(self.selection.get())
