# A frame which contains a panel of Buttons with various 'Shortcut' functions.

from idlelib.tooltip import Hovertip
from tkinter import ttk

from core.graphics.main import main_frame
from core.services import files


# widget frame
widget: ttk.Frame

# shortcut buttons
run_button: ttk.Button
clear_button: ttk.Button
audio_hr_button: ttk.Button
video_hr_button: ttk.Button
save_ask_btn: ttk.Button
save_auto_btn: ttk.Button
set_savedir_btn: ttk.Button


def build(parent):
    global widget
    widget = ttk.Frame(parent)
    widget.pack(side='top', fill='x')

    s = ttk.Style()
    s.configure('scut.TButton', font=12)

    # 25BA
    global run_button
    run_button = ttk.Button(widget, text='\u25B6', width=2, style='scut.TButton', command=Run)
    run_button.pack(side='left', padx=1)
    Hovertip(run_button, '@Run: Execute the current process.')

    # \u2421
    global clear_button
    clear_button = ttk.Button(widget, text='\u2326', width=2, style='scut.TButton', command=Clear)
    clear_button.pack(side='left', padx=1)
    Hovertip(clear_button, '@Clear: Clears output frame.')

    # Separator
    ttk.Separator(widget, orient='vertical').pack(side='left', padx=8, fill='y')

    global audio_hr_button
    audio_hr_button = ttk.Button(widget, text='\u266B', width=2, style='scut.TButton')
    audio_hr_button.pack(side='left', padx=1)
    Hovertip(audio_hr_button, '@Audio: @Run \u27A1 Automatically download\naudio at highest resolution.')

    global video_hr_button
    video_hr_button = ttk.Button(widget, text='\u2B73', width=2, style='scut.TButton')
    video_hr_button.pack(side='left', padx=1)
    Hovertip(video_hr_button, '@Video: @Run \u27A1 Automatically download\nvideo & audio at highest '
                              'resolution.')

    # Separator
    ttk.Separator(widget, orient='vertical').pack(side='left', padx=8, fill='y')

    global save_ask_btn
    save_ask_btn = ttk.Button(widget, text='?F', width=2, style='scut.TButton',
                              command=lambda: Save(True))
    save_ask_btn.configure(state='disabled')
    save_ask_btn.pack(side='left', padx=1)
    Hovertip(save_ask_btn, '*Save=Ask: When downloading, you \nwill be prompted for a save location.')

    global save_auto_btn
    save_auto_btn = ttk.Button(widget, text='\u25B8F', width=2, style='scut.TButton',
                               command=lambda: Save(False))
    save_auto_btn.pack(side='left', padx=1)
    Hovertip(save_auto_btn, '*Save=Auto: When downloading,\nfiles save straight to *SaveDir.')

    global set_savedir_btn
    set_savedir_btn = ttk.Button(widget, text='\u21B3F', width=3, style='scut.TButton',
                                 command=files.prompt_update_default_save_directory)
    set_savedir_btn.pack(side='left', padx=1)
    Hovertip(set_savedir_btn, '*SaveDir: Select a location to\nautomatically save to.')


def disable_button(button):
    button.configure(state='disabled')


def enable_button(button):
    button.configure(state='enabled')


# executed when a new process is scheduled.
# disables some shortcuts.
def block_new_processes():
    disable_button(run_button)
    disable_button(clear_button)


def unblock_new_processes():
    enable_button(run_button)
    enable_button(clear_button)


def Run():
    main_frame.schedule_load_media()


def Clear():
    main_frame.clear()


# Updates the Save Mode between ASK and AUTO, disabling the selected button.
def Save(ask):
    files.prompt_for_downloads = ask
    # If ASK mode, disable the ASK button.
    if ask:
        disable_button(save_ask_btn)
        enable_button(save_auto_btn)
    else:
        disable_button(save_auto_btn)
        enable_button(save_ask_btn)
