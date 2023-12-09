# Multimedia Utility Download Tool (Deprecated)

## Notice: This project is now deprecated.
MUD Tool will no longer be maintained by PyroNeon Software. Development on this project is being indefinitely suspended.

## Alternative Programs:
- FetchV (<a href="https://chromewebstore.google.com/detail/fetchvvideo-downloaderhls/imleiiaoeclikefimmcdkjabjbpcdgaj">Chrome Store</a>)
A very powerful chrome/edge extension which automatically scans webpages for m3u8, blob, or mp4 video stream sources, and provides a simple, user-friendly GUI to download files. It is very effective, completely free, and non-intrusive. I (JLeopolt) personally use this extension, and it captures exactly what MUD Tool should have been.
- yt-dlp (<a href="https://github.com/yt-dlp/yt-dlp">GitHub Page</a>)
An extremely versatile CLI youtube downloader. It provides an endless amount of options and parameters, meant for power users. When it comes to downloading from youtube, this is by far the best tool, although it would be quite difficult for a novice or casual user to grasp. If you're a power user or developer, this is the perfect solution for you.
- Media Downloader (<a href="https://github.com/mhogomchungu/media-downloader">GitHub Page</a>)
A user-friendly GUI alternative to yt-dlp. This software is basically just a fancy GUI wrapper for yt-dlp, but it really is a lot simpler to use. It has good configuration support and allows you to do things like download bulk youtube playlists or hundreds of videos at a time automatically, without having to figure out all of the command options like with yt-dlp. Highly recommended for normal people and non-devs.

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
* Overhaul scanning feature.
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

## Contact Us
If you have any inquiries, contact us <a href="https://www.pyroneon.net/contact-us/email">here</a>.<br>
Visit the official website for MUD Tool <a href="https://www.pyroneon.net/experimental/mudtool">here</a>.

### Disclaimer:
Please do not illegally download copyrighted content such as music or movies using this software.
