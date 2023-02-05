from idlelib.tooltip import Hovertip
from tkinter import ttk
from core.services import files


def disable(button):
    button.configure(state='disabled')


def enable(button):
    button.configure(state='enabled')


# A frame which contains a panel of Buttons with various 'Shortcut' functions.
class Shortcuts(ttk.Frame):
    # URL Mode defaults to YouTube
    URL_Mode = 0

    def __init__(self, youtubetab, container):
        super().__init__(container)

        self.youtube_tab = youtubetab
        self.src = container

        s = ttk.Style()
        s.configure('scut.TButton', font=12)

        # 25BA
        self.run_button = ttk.Button(self, text='\u25B6', width=2, style='scut.TButton', command=self.Run)
        self.run_button.pack(side='left', padx=1)
        Hovertip(self.run_button, '@Run: Execute the current process.')

        # \u2421
        self.clear_button = ttk.Button(self, text='\u2326', width=2, style='scut.TButton', command=self.Clear)
        self.clear_button.pack(side='left', padx=1)
        Hovertip(self.clear_button, '@Clear: Clears output frame.')

        # Separator
        ttk.Separator(self, orient='vertical').pack(side='left', padx=8, fill='y')

        self.audio_hr_button = ttk.Button(self, text='\u266B', width=2, style='scut.TButton')
        self.audio_hr_button.pack(side='left', padx=1)
        Hovertip(self.audio_hr_button, '@Audio: @Run \u27A1 Automatically download\naudio at highest resolution.')

        self.video_hr_button = ttk.Button(self, text='\u2B73', width=2, style='scut.TButton')
        self.video_hr_button.pack(side='left', padx=1)
        Hovertip(self.video_hr_button, '@Video: @Run \u27A1 Automatically download\nvideo & audio at highest '
                                       'resolution.')

        # Separator
        ttk.Separator(self, orient='vertical').pack(side='left', padx=8, fill='y')

        # Set URL MODE to YouTube
        self.youtube_button = ttk.Button(self, text='\u25B6\u2261', width=2, style='scut.TButton',
                                         command=lambda: self.set_URL_mode(0))
        self.youtube_button.pack(side='left', padx=1)
        Hovertip(self.youtube_button, '*Mode=YouTube: Treat the input as a YouTube URL.')
        # selected by default
        disable(self.youtube_button)

        # Set URL MODE to BLOB direct
        self.blob_button = ttk.Button(self, text='B\u2261', width=2, style='scut.TButton',
                                      command=lambda: self.set_URL_mode(1))
        self.blob_button.pack(side='left', padx=1)
        Hovertip(self.blob_button, '*Mode=BLOB: Treat the input as a BLOB URL.')

        # Set URL MODE to BLOB direct
        self.files_button = ttk.Button(self, text='F\u2261', width=2, style='scut.TButton',
                                       command=lambda: self.set_URL_mode(2))
        self.files_button.pack(side='left', padx=1)
        Hovertip(self.files_button, '*Mode=FILE: Treat the input as a file URL.')

        # Set URL MODE to Auto
        self.scan_button = ttk.Button(self, text='?\u2261', width=2, style='scut.TButton',
                                      command=lambda: self.set_URL_mode(3))
        self.scan_button.pack(side='left', padx=1)
        Hovertip(self.scan_button, '*Mode=Scan: Scan the input, looking for\nmedia files or BLOB URLs.')

        # Separator
        ttk.Separator(self, orient='vertical').pack(side='left', padx=8, fill='y')

        self.save_ask_btn = ttk.Button(self, text='?F', width=2, style='scut.TButton',
                                       command=lambda: self.Save(True))
        self.save_ask_btn.configure(state='disabled')
        self.save_ask_btn.pack(side='left', padx=1)
        Hovertip(self.save_ask_btn, '*Save=Ask: When downloading, you \nwill be prompted for a save location.')

        self.save_auto_btn = ttk.Button(self, text='\u25B8F', width=2, style='scut.TButton',
                                        command=lambda: self.Save(False))
        self.save_auto_btn.pack(side='left', padx=1)
        Hovertip(self.save_auto_btn, '*Save=Auto: When downloading,\nfiles save straight to *SaveDir.')

        self.set_savedir_btn = ttk.Button(self, text='\u21B3F', width=3, style='scut.TButton',
                                          command=lambda: files.prompt_update_default_save_directory(
                                              youtubetab.console))
        self.set_savedir_btn.pack(side='left', padx=1)
        Hovertip(self.set_savedir_btn, '*SaveDir: Select a location to\nautomatically save to.')

    def set_URL_mode(self, mode):
        self.URL_Mode = mode

        # youtube mode
        if mode == 0:
            disable(self.youtube_button)
            enable(self.blob_button)
            enable(self.scan_button)
            enable(self.files_button)
        # Blob mode
        elif mode == 1:
            disable(self.blob_button)
            enable(self.youtube_button)
            enable(self.scan_button)
            enable(self.files_button)
        # File mode
        elif mode == 2:
            disable(self.files_button)
            enable(self.youtube_button)
            enable(self.scan_button)
            enable(self.blob_button)
        # Scan mode
        elif mode == 3:
            disable(self.scan_button)
            enable(self.youtube_button)
            enable(self.blob_button)
            enable(self.files_button)

    # executed when a new process is scheduled.
    # disables some shortcuts.
    def block_new_processes(self):
        disable(self.run_button)
        disable(self.clear_button)

    def unblock_new_processes(self):
        enable(self.run_button)
        enable(self.clear_button)

    def Run(self):
        self.youtube_tab.schedule_load_media()

    def Clear(self):
        self.youtube_tab.Clear()

    # Updates the Save Mode between ASK and AUTO, disabling the selected button.
    def Save(self, ask):
        files.prompt_for_downloads = ask
        # If ASK mode, disable the ASK button.
        if ask:
            self.save_ask_btn.configure(state='disabled')
            self.save_auto_btn.configure(state='enabled')
        else:
            self.save_auto_btn.configure(state='disabled')
            self.save_ask_btn.configure(state='enabled')
