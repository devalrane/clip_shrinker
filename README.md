# Clip Shrinker

A Python-based GUI for Efficient Video Compression

This Python application was born out of a personal need to share large video files captured during late-night gaming sessions. Designed for casual gamers, it offers a user-friendly interface for uploading and compressing video content, significantly reducing file size without compromising quality. With a compression rate of 92%, this tool enables seamless sharing of even the most substantially large video files.

Supported formats: `mp4`, `mkv`, `.avi`

## Features

- Easy File Selection: Upload single or multiple video files for compression.
- Thumbnail Preview: View thumbnails of selected videos.
- Progress Tracking: Real-time progress bars show compression progress for each video.
- Compressed Files Directory: Open the directory where compressed files are stored directly from the app.
- Plug-and-Play: Built to run on Windows systems without requiring a separate Python or dependency installation.

## Technologies Used

- Python: Main programming language.
- Tkinter: GUI toolkit for building the application interface.
- FFmpeg: For video compression and thumbnail extraction.
- Pillow: For handling image processing (thumbnails).

## Installation

### Running the Application

To run the application on your local machine, download the executable file, `clip_shrinker.exe`, in the dist folder.

### Running the Project:

1. Clone the Repository:

   ```
   git clone https://github.com/devalrane/clip_shrinker.git
   cd clip_shrinker
   ```

2. Install Required Packages:
   Ensure you have Python installed, then install the required packages using pip:

   ```
   pip install -r requirements.txt
   ```

3. Run the Application:
   Execute the script:
   ```
   python clip_shrinker.py
   ```

## Usage

1. Select Files: Click on the "Select Files" button to choose video files (MP4, MKV, AVI) for compression.
2. View Thumbnails: After selection, thumbnails of the videos will be displayed along with their names.
3. Monitor Progress: As compression takes place, the progress bar will indicate the percentage of completion for each file.
4. Open Compressed Files: Use the "Open Compressed Files" button to view the directory where compressed videos are saved.

## Packaging as an Executable

To package the application as a standalone executable for Windows, you can use PyInstaller. Follow these steps:

1. Install PyInstaller:

   ```
   pip install pyinstaller
   ```

2. Build the Executable:
   Run the following command:

   ```
   pyinstaller --onefile --windowed --icon="path/to/icon.ico" clip_shrinker.py
   ```

3. Find the Executable: The executable will be located in the `dist` directory.

## Contribution

Contributions are welcome! If you find any issues or would like to suggest improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FFmpeg for the powerful video processing capabilities.
- Tkinter for providing the GUI framework.
- Pillow for picking the thumbnail.
