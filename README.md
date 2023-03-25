# Multimedia Utility Download Tool

## About
MUD Tool (Multimedia Utility Download Tool) is a powerful program which allows you to download and convert media files from the web. If you've ever been browsing the web and wanted to download a video, but it's locked behind a paywall or asks you to sign up to download, just use the MUD Tool!

## Features
MUD offers native support for YouTube videos, giving you full control over what streams to use when downloading, output file types, etc. MUD is also able to scan the HTML contents of a website you provide, and pick out video files straight from the source, so you can download anything without having to sign up for an account.

## Downloading (For Use)
Simply select the latest version of the program from the Releases section, and download the attached .EXE file.
All code, assets, and dependencies are bundled in the .EXE file, so it'll be ready to use immediately.

### Downloading (For Testing/Development)
1. Install the latest version of <a href="https://www.python.org/downloads/">Python</a>. <br>
2. Install and open Git Bash. <br>
3. In Git Bash, navigate to the directory where you want the project installed.
```
cd C:\Your\Specific\Directory
```
4. Then, clone this repository.
```
git clone https://github.com/JLeopolt/MultimediaUtilityDownloadTool.git
```
5. Install <a href="https://ffmpeg.org/download.html">FFMPEG</a> as a .ZIP or .7z archive file. <br>
6. Open the FFMPEG archive file with a ZIP extractor tool like <a href="https://www.win-rar.com/start.html?&L=0">WinRAR</a>. <br>
7. Navigate to the "bin" folder inside the archived file. <br>
8. Right click the "ffmpeg.exe" file, and select "extract to directory". <br>
9. Extract the "ffmpeg.exe" file into the "MultimediaUtilityDownloadTool" directory that was created when you cloned the github repository. 
It should be in the SAME FOLDER as the "__ main __.py" file!
```
(Your directory from Step 3)
. 
├─ MultimediaUtilityDownloadTool
├── core
├─── '__main__.py'
└─── 'ffmpeg.exe'
```
10. To launch the program, just run "__ main __.py"!

## To-Do List
* Add support for custom plugins.
* Allow users to save and import/export settings.
* Allow users to input custom FFMPEG flags for operations.
* Support for YouTube playlists and automating URL input.
* Support output media file metadata tagging with FFMPEG.

## Authors
[JLeopolt](https://github.com/JLeopolt) - *Developer*

## License
This project is licensed under **GNU GPL-3.0** - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
* Thanks to [pytube](https://github.com/pytube/pytube) for their YouTube API.
* Thanks to FFMPEG for their amazing software.
<br><b>Disclaimer:</b><br>
Please do not illegally download copyrighted content such as music or movies using this software.<br>
If you have any inquiries, contact us <a href="https://www.pyroneon.ml/contact-us/email">here</a>.<br>
Visit the official website for MUD Tool <a href="https://www.pyroneon.ml/mudtool">here</a>.<br>
