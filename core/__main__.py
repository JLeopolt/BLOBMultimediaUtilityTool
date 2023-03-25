# A multimedia utility downloader and converter tool which can download media sources from the Web.

import core
import core.gui.gui as gui
import sys


def get_software_details():
    return "Multimedia Utility Download Tool v" + core.__version__


def get_license_details():
    return "Copyright (c) 2023 PyroNeon Software. Licensed under GPL-3.0 License."


def get_python_version():
    return sys.version.split(" ")[0]


if __name__ == '__main__':
    gui.run()
