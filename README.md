# YouTube Downloader GUI using Tkinter

This project is a graphical user interface (GUI) application built with Python's Tkinter library to download YouTube videos and playlists. It provides an easy-to-use interface to input URLs of YouTube videos or playlists, select desired video resolutions, choose download destination, and initiate the downloading process. The downloaded videos are saved in the selected destination folder in the specified resolution.

## Features

- Download individual YouTube videos or entire playlists.
- Choose from available video resolutions (1080p, 720p, 480p).
- Select the destination folder for downloaded videos.
- Visual progress bar to track the download process.
- Built-in merging of audio and video streams using FFmpeg.

## Requirements

- Python 3.x
- Tkinter
- ttkthemes
- PIL (Pillow)
- pytube
- moviepy
- FFmpeg (must be installed and accessible in the system environment)

## Installation

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/kourdroid/youtubify.git
   cd youtubify
   ```

2. Install the required Python packages using pip:

   ```
   pip install -r requirements.txt
   ```

3. Make sure you have FFmpeg installed. If not, download it from the official website and add its path to the system environment variables.

## Usage

1. Run the application by executing the following command:

   ```
   python main.py
   ```

2. The main window of the application will appear, showing two buttons: "Playlist Downloader" and "Video Downloader."

3. Click the appropriate button based on whether you want to download a playlist or a single video.

4. A new window will open with options to input the URL, select the desired resolution, and choose the destination folder.

5. Click the "CHOOSE FOLDER" button to set the destination for the downloaded files.

6. After selecting all the required options, click the "DOWNLOAD PLAYLIST" or "DOWNLOAD VIDEO" button to initiate the download.

7. A progress bar will show the download progress. Once the download is complete, a success message will be displayed.

## Notes

- This application uses the pytube library to interact with YouTube's servers and download videos. Keep in mind that YouTube's API and website structure can change over time, which might affect the functionality of the application.
- The moviepy library is used for merging audio and video streams. Ensure that FFmpeg is properly installed and configured in your environment for this process to work correctly.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This project is intended for educational and personal use only. Downloading copyrighted content without permission from the content owner may violate YouTube's terms of service and copyright laws in your region. Use this tool responsibly and respect the rights of content creators. The project authors are not responsible for any misuse or legal consequences resulting from the use of this tool.
