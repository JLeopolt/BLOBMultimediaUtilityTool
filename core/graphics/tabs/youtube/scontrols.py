from idlelib.tooltip import Hovertip
from tkinter import ttk
from core.services import files


# A frame which contains a panel of Buttons with various 'Shortcut' functions.
class Shortcuts(ttk.Frame):

    def __init__(self, container, console):
        super().__init__(container)

        s = ttk.Style()
        s.configure('scut.TButton', font=('Helvetica', 12))

        self.run_button = ttk.Button(self, text='\u25BA', width=2, style='scut.TButton')
        self.run_button.pack(side='left', padx=1)
        Hovertip(self.run_button, '@Run: Execute the current script.')

        self.stop_button = ttk.Button(self, text='\u2715', width=2, style='scut.TButton')
        self.stop_button.pack(side='left', padx=1)
        Hovertip(self.stop_button, '@Stop: Terminate current process.')

        self.clear_button = ttk.Button(self, text='\u2421', width=2, style='scut.TButton')
        self.clear_button.pack(side='left', padx=1)
        Hovertip(self.clear_button, '@Clear: Perform @Stop, then\nclear output frame.')

        # Separator
        ttk.Separator(self, orient='vertical').pack(side='left', padx=8, fill='y')

        self.audio_hr_button = ttk.Button(self, text='\u266B', width=2, style='scut.TButton')
        self.audio_hr_button.pack(side='left', padx=1)
        Hovertip(self.audio_hr_button, '@Audio.HR: @Run + Automatically download\naudio at highest resolution.')

        self.video_hr_button = ttk.Button(self, text='\u2B73', width=2, style='scut.TButton')
        self.video_hr_button.pack(side='left', padx=1)
        Hovertip(self.video_hr_button, '@Video.HR: @Run + Automatically download\nvideo & audio at highest resolution.')

        # Separator
        ttk.Separator(self, orient='vertical').pack(side='left', padx=8, fill='y')

        self.save_ask_btn = ttk.Button(self, text='?F', width=2, style='scut.TButton',
                                       command=lambda: self.update_save_mode(True))
        self.save_ask_btn.configure(state='disabled')
        self.save_ask_btn.pack(side='left', padx=1)
        Hovertip(self.save_ask_btn, '*Save=ASK: When downloading,\nyou will be prompted for a save location.')

        self.save_auto_btn = ttk.Button(self, text='\u25B8F', width=2, style='scut.TButton',
                                        command=lambda: self.update_save_mode(False))
        self.save_auto_btn.pack(side='left', padx=1)
        Hovertip(self.save_auto_btn, '*Save=AUTO: When downloading,\nfiles save to your chosen folder.')

        self.set_savedir_btn = ttk.Button(self, text='\u21B3F', width=2, style='scut.TButton',
                                          command=lambda: files.prompt_update_default_save_directory(console))
        self.set_savedir_btn.pack(side='left', padx=1)
        Hovertip(self.set_savedir_btn, '*SaveDir: Select a location to\nautomatically save to.')

    # Updates the Save Mode between ASK and AUTO, disabling the selected button.
    def update_save_mode(self, ask):
        files.prompt_for_downloads = ask
        # If ASK mode, disable the ASK button.
        if ask:
            self.save_ask_btn.configure(state='disabled')
            self.save_auto_btn.configure(state='enabled')
        else:
            self.save_auto_btn.configure(state='disabled')
            self.save_ask_btn.configure(state='enabled')
