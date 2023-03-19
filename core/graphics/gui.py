import tkinter as tk
import webbrowser
from tkinter import ttk

from core import __main__ as mainpy
from core.graphics.common import console
from core.graphics.main import main_frame

# The main application window.
root: tk.Tk


# Called to build the window on application launch.
def run():
    global root
    root = tk.Tk()

    # root window
    root.title(mainpy.get_software_details())
    root.geometry('600x700')
    style = ttk.Style(root)

    # create window icon
    ico = tk.PhotoImage(file="assets/icon.png")
    root.wm_iconphoto(False, ico)

    # create main frame
    main_frame.build(root)

    # menubar config
    configure_menubar(style)

    # finally, execute the window
    root.mainloop()


# helper method which sets up the top Menubar of the window.
def configure_menubar(style):
    # Create menubar
    menubar = tk.Menu(root)

    # Prepare 'File' menu
    file_menu = tk.Menu(menubar, tearoff=0)

    # 'Styles' submenu
    themes_submenu = tk.Menu(file_menu, tearoff=0)
    # Add all theme options
    for theme_name in style.theme_names():
        themes_submenu.add_command(label=theme_name, command=lambda t=theme_name: style.theme_use(t))
    file_menu.add_cascade(label="Styles", menu=themes_submenu)

    # 'Console' submenu
    console_submenu = tk.Menu(file_menu, tearoff=0)
    # clears the console
    console_submenu.add_command(label="Clear", command=console.clear)
    # saves a log of the console
    console_submenu.add_command(label="Save History", command=console.save_log)
    file_menu.add_cascade(label="Console", menu=console_submenu)

    file_menu.add_separator()
    # exits the program
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    # Prepare HelpMenu
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=lambda: webbrowser.open('https://www.pyroneon.ml/mudtool'))
    menubar.add_cascade(label="Help", menu=help_menu)

    # Add the Menu to window
    root.config(menu=menubar)
