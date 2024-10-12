import tkinter as tk
from tkinter import filedialog, messagebox
import ffmpeg
import os


# Function to compress video files
def compress_videos(files):
    # Get the current directory
    current_directory = os.getcwd()

    # Create a new directory for compressed files if it doesn't exist
    compressed_folder = os.path.join(current_directory, "compressed_files")
    if not os.path.exists(compressed_folder):
        os.makedirs(compressed_folder)

    # Process each selected video file
    for ip_file_path in files:
        try:
            # Extract the file name
            file_name = os.path.basename(ip_file_path)
            print(f"Processing: {file_name}")

            # Create input stream
            stream = ffmpeg.input(ip_file_path)

            # Separate video and audio streams
            stream_video = stream.video
            stream_audio = stream.audio

            # Output file path in the compressed_files folder
            output_file = os.path.join(compressed_folder, "WA_" + file_name)

            # Prepare ffmpeg output with video and audio compression
            stream_op = ffmpeg.output(
                stream_video,
                stream_audio,
                output_file,
                vcodec="libx265",
                acodec="aac",  # Explicit audio codec
                preset="fast",
            )

            # Overwrite the output if it already exists
            stream_op = stream_op.overwrite_output()

            # Run the ffmpeg command
            ffmpeg.run(stream_op)

            print(f"Compressed video saved as: {output_file}")
        except ffmpeg.Error as e:
            print(
                f"An error occurred while processing {file_name}: {e.stderr.decode()}"
            )
            messagebox.showerror("Compression Error", f"Failed to compress {file_name}")

    # Show completion message
    messagebox.showinfo("Success", "All selected videos have been compressed.")


# Function to allow the user to select video files
def select_files():
    filetypes = [("Video files", "*.mp4 *.mkv *.avi *.mov"), ("All files", "*.*")]
    files = filedialog.askopenfilenames(title="Select Video Files", filetypes=filetypes)
    if files:
        compress_videos(files)
    else:
        messagebox.showwarning(
            "No Files Selected", "Please select at least one video file to compress."
        )


# Create the main tkinter window
root = tk.Tk()
root.title("Video Compressor")
root.geometry("400x200")

# Create and place the label
label = tk.Label(root, text="Select video files to compress", font=("Arial", 14))
label.pack(pady=20)

# Create and place the "Select Files" button
select_button = tk.Button(
    root, text="Select Files", command=select_files, font=("Arial", 12)
)
select_button.pack(pady=10)

# Start the tkinter event loop
root.mainloop()
