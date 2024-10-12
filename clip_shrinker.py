import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import threading
import os
import ffmpeg
import subprocess


# Function to extract thumbnail for each video
def extract_thumbnail(file_path, thumbnail_path):
    try:
        (
            ffmpeg.input(file_path, ss="00:00:01")
            .filter("scale", 200, -1)
            .output(thumbnail_path, vframes=1)
            .overwrite_output()
            .run(quiet=True)
        )
        return thumbnail_path
    except ffmpeg.Error as e:
        print(f"Error extracting thumbnail: {e.stderr.decode()}")
        return None


# Function to compress a single video file with progress tracking
def compress_video(file_path, progress_bar, progress_label, status_label):
    try:
        compressed_folder = "compressed_files"
        if not os.path.exists(compressed_folder):
            os.makedirs(compressed_folder)

        output_file = os.path.join(compressed_folder, os.path.basename(file_path))

        command = [
            "ffmpeg",
            "-i",
            file_path,
            "-vcodec",
            "libx265",
            "-acodec",
            "aac",
            "-preset",
            "fast",
            "-y",
            output_file,
        ]

        process = subprocess.Popen(
            command, stderr=subprocess.PIPE, universal_newlines=True
        )

        total_duration = None
        for line in process.stderr:
            if "Duration" in line:
                # Extract total duration from the ffmpeg output
                total_duration = get_duration(line)
            elif "frame=" in line and total_duration:
                # Parse progress and update progress bar
                progress = get_progress(line, total_duration)
                progress_bar["value"] = progress
                progress_label.config(
                    text=f"{progress:.2f}%"
                )  # Update the progress label
                root.update_idletasks()

        process.wait()

        status_label.config(text="Compression Complete!")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")


# Function to calculate video duration from ffmpeg output
def get_duration(duration_line):
    try:
        parts = duration_line.split(",")
        time_part = parts[0].split()[1]  # Get the time part "00:00:10.00"
        h, m, s = time_part.split(":")  # Ensure it has 3 parts (HH:MM:SS)
        return int(h) * 3600 + int(m) * 60 + float(s)
    except ValueError as e:
        print(f"Error parsing duration: {e}")
        return None


# Function to calculate progress based on the ffmpeg output
def get_progress(progress_line, total_duration):
    try:
        parts = progress_line.split()
        time_str = None
        for part in parts:
            if part.startswith("time="):
                time_str = part.split("=")[1]
                break

        if time_str:
            time_parts = time_str.split(":")
            if len(time_parts) == 3:  # Ensure it's a valid time format (HH:MM:SS)
                h, m, s = time_parts
                current_time = int(h) * 3600 + int(m) * 60 + float(s)
                return (current_time / total_duration) * 100
        return 0
    except ValueError as e:
        print(f"Error parsing progress: {e}")
        return 0


# Function to start the compression in a separate thread
def start_compression(files):
    for file_path in files:
        # Create a thumbnail for the video
        thumbnail_path = os.path.join(
            "thumbnails", f"thumbnail_{os.path.basename(file_path)}.png"
        )
        thumbnail = extract_thumbnail(file_path, thumbnail_path)

        # Display the thumbnail and progress bar
        if thumbnail:
            image = Image.open(thumbnail)
            image = image.resize(
                (200, int(image.height * 200 / image.width)), Image.ANTIALIAS
            )
            image = ImageTk.PhotoImage(image)

            # Create a frame for each video item
            video_frame = tk.Frame(root)
            video_frame.pack(pady=5)

            # Create a label for the thumbnail
            thumbnail_label = tk.Label(video_frame, image=image)
            thumbnail_label.image = image  # Keep a reference
            thumbnail_label.grid(row=0, column=0)

            # Create a label for the filename
            filename_label = tk.Label(
                video_frame, text=os.path.basename(file_path), wraplength=200
            )
            filename_label.grid(row=1, column=0)

            # Add a progress bar
            progress_bar = ttk.Progressbar(
                video_frame, orient="horizontal", length=300, mode="determinate"
            )
            progress_bar.grid(row=0, column=1, padx=10)

            # Add a label to show progress percentage inside the bar
            progress_label = tk.Label(video_frame, text="0.00%", width=5)
            progress_label.grid(row=0, column=1)  # Position over the progress bar

            # Add a status label
            status_label = tk.Label(root, text="Starting compression...")
            status_label.pack()

            # Start compression in a new thread
            threading.Thread(
                target=compress_video,
                args=(file_path, progress_bar, progress_label, status_label),
            ).start()


# Function to browse and select files
def browse_files():
    files = filedialog.askopenfilenames(
        filetypes=[("Video Files", "*.mp4 *.mkv *.avi")]
    )
    if files:
        start_compression(files)


# Create the GUI
root = tk.Tk()
root.title("Video Compressor")

label = tk.Label(root, text="Select video files to compress")
label.pack(pady=10)

select_button = tk.Button(root, text="Select Files", command=browse_files)
select_button.pack(pady=5)

root.mainloop()
