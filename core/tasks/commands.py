from core.gui.main import main_frame


# Resets the window.
def Clear():
    main_frame.clear()


# Executes the selected process.
def Run():
    main_frame.schedule_load_media()
