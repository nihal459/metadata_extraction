from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image
from PIL.ExifTags import TAGS
from moviepy.editor import VideoFileClip
import pikepdf
from tinytag import TinyTag


def extract_image_metadata(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img.getexif()

        metadata = {}
        if exif_data is not None:
            for tagid, value in exif_data.items():
                tag = TAGS.get(tagid, tagid)
                metadata[tag] = value

        return metadata

    except Exception as e:
        print(f"Error extracting image metadata: {e}")
        return None


def extract_video_metadata(video_path):
    try:
        # Load the video clip
        video_clip = VideoFileClip(video_path)

        # Extract metadata
        metadata = {
            'duration': video_clip.duration,
            'fps': video_clip.fps,
            'size': video_clip.size,
            'audio': {
                'channels': video_clip.audio.nchannels,
                'sample_rate': video_clip.audio.fps,
                'duration': video_clip.audio.duration,
            },
            'video_framecount': video_clip.reader.nframes,
            'video_duration': video_clip.reader.duration,
            'video_rotation': video_clip.rotation,
            'audio_frames': video_clip.audio.fps * video_clip.audio.duration,
            'has_mask': video_clip.mask is not None,
            'has_audio': video_clip.audio is not None,
            'audio_channels': video_clip.audio.nchannels if video_clip.audio is not None else None,
            'video_file_path': video_path,
        }

        return metadata

    except Exception as e:
        print(f"Error extracting video metadata: {e}")
        return None


def extract_pdf_metadata(pdf_path):
    try:
        pdf = pikepdf.Pdf.open(pdf_path)
        pdf_metadata = pdf.docinfo
        return dict(pdf_metadata)

    except Exception as e:
        print(f"Error extracting PDF metadata: {e}")
        return None


def extract_audio_metadata(audio_path):
    try:
        tag = TinyTag.get(audio_path)
        metadata = {
            'title': tag.title,
            'artist': tag.artist,
            'album': tag.album,
            'year': tag.year,
            'duration': tag.duration,
            'sample_rate': tag.samplerate,
            'bitrate': tag.bitrate,
            'channels': tag.channels,
            'genre': tag.genre,
        }
        return metadata

    except Exception as e:
        print(f"Error extracting audio metadata: {e}")
        return None


def extract_metadata_and_show_window():
    file_path = code.get()
    selected_type = selected_format.get()

    if file_path:
        if selected_type == "Image":
            metadata = extract_image_metadata(file_path)
            if metadata:
                show_metadata_window("Image Metadata", metadata)
            else:
                show_error_message("Metadata extraction failed for image.")

        elif selected_type == "Video":
            metadata = extract_video_metadata(file_path)
            if metadata:
                show_metadata_window("Video Metadata", metadata)
            else:
                show_error_message("Metadata extraction failed for video.")

        elif selected_type == "PDF":
            metadata = extract_pdf_metadata(file_path)
            if metadata:
                show_metadata_window("PDF Metadata", metadata)
            else:
                show_error_message("Metadata extraction failed for PDF.")

        elif selected_type == "Audio":
            metadata = extract_audio_metadata(file_path)
            if metadata:
                show_metadata_window("Audio Metadata", metadata)
            else:
                show_error_message("Metadata extraction failed for audio.")

        else:
            show_error_message("Invalid file format. Please select 'Image', 'Video', 'PDF', or 'Audio'.")

    else:
        show_error_message("Invalid file path.")


def show_metadata_window(title, metadata):
    metadata_window = Toplevel(screen)
    metadata_window.title(title)
    metadata_window.geometry("375x450")
    image_icon = PhotoImage(file="data.png")
    metadata_window.iconphoto(False, image_icon)
    text_widget = Text(metadata_window, wrap=WORD)
    text_widget.insert(END, f"{title}:\n\n")
    for key, value in metadata.items():
        text_widget.insert(END, f"{key}: {value}\n")
    text_widget.pack(expand=YES, fill=BOTH)


def show_error_message(message):
    error_label = Label(screen, text=message, fg="red", font=("calbri", 13))
    error_label.place(x=25, y=390)  # Adjust the y-coordinate
    screen.after(3000, error_label.destroy)  # Automatically remove the error message after 3000 milliseconds


def main_screen():
    global screen
    global code
    global text1
    global selected_format

    screen = Tk()
    screen.geometry("375x450")

    image_icon = PhotoImage(file="data.png")
    screen.iconphoto(False, image_icon)

    screen.title("Metadata Extraction Application")

    # Load the image above the "Select file format" label
    image_path_above_label = "bluebg.png"  # Replace with the actual path to your image
    image_above_label = PhotoImage(file=image_path_above_label)

    # Get the size of the image
    img_width = image_above_label.width()
    img_height = image_above_label.height()

    # Resize the image
    new_width = 250  # Adjust the width as needed
    new_height = int((new_width / img_width) * img_height)
    image_above_label = image_above_label.subsample(int(img_width / new_width), int(img_height / new_height))

    label_above = Label(screen, image=image_above_label)
    label_above.place(relx=0.5, rely=0.25, anchor=CENTER)  # Adjust the rely value to position the image above

    Label(text="Select file format:", fg="black", font=("calbri", 13)).place(x=10, y=220)  # Adjust the y-coordinate

    file_formats = ["Select File", "Audio", "Video", "PDF", "Image"]
    selected_format = StringVar()
    dropdown = ttk.Combobox(screen, textvariable=selected_format, values=file_formats, state="readonly", font=("calibri", 12), width=24)
    dropdown.place(x=150, y=220)  # Adjust the y-coordinate
    dropdown.set(file_formats[0])  # Set the default selection

    code = StringVar()

    Label(text="Select a file:", fg="black", font=("calbri", 13)).place(x=10, y=270)  # Adjust the y-coordinate
    
    def choose_file():
        file_path = filedialog.askopenfilename()
        code.set(file_path)

    Button(text="Choose File", height="2", width=30, bg="#00bd56", fg="white", bd=0, command=choose_file).place(x=150, y=260)  # Adjust the y-coordinate

    Button(text="EXTRACT METADATA", height="2", width=50, bg="#1089ff", fg="white", bd=0, command=extract_metadata_and_show_window).place(x=10, y=330)  # Adjust the y-coordinate

    screen.mainloop()

main_screen()
