# An open-source multimedia utility downloader and converter tool which can download media sources from the Web.

import core
import core.graphics.gui as gui


def print_software_details():
    print("BLOB Multimedia Utility Tool v" + core.__version__)
    print("Copyright (c) 2023 PyroNeon Software. Licensed under GPL 3.0")


if __name__ == '__main__':
    print_software_details()
    gui.App().mainloop()
