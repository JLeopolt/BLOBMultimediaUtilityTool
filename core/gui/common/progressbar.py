import tkinter.ttk as ttk
from core.utility import utils


class ProgressBar(ttk.Frame):
    progress_bar = None

    def __init__(self, container):
        super().__init__(container)

    def start(self):
        utils.destroy_children(self)
        # add a progress bar into the frame
        self.progress_bar = ttk.Progressbar(self, orient='horizontal', mode='indeterminate')
        self.progress_bar.start()
        self.progress_bar.pack(side='top', expand=True, fill='x', anchor='nw')

    def stop(self):
        if self.progress_bar is not None:
            self.progress_bar.pack_forget()
            self.progress_bar.destroy()
        ttk.Frame(self, width=1, height=1, borderwidth=0).pack()
