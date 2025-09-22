import os
import argparse
import cv2
from PIL import Image, ImageFilter

# Colors
RED = "\033[31m"
GREEN = "\033[92m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# Function to process video files and create blurred images
def process_video(video_path, blur_radius):
    try:
        # Open the video file with cv2.CAP_FFMPEG backend
        cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)

        # Suppress "Unsupported encoding type" warning
        with open(os.devnull, 'w') as null:
            stderr_backup = os.dup(2)
            os.dup2(null.fileno(), 2)

            # Get total number of frames and frame rate
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)

            # Calculate the middle frame number
            middle_frame_number = total_frames // 2

            # Set the frame position to the middle frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_number)

            # Read the frame
            ret, frame = cap.read()

            # Restore stderr
            os.dup2(stderr_backup, 2)
            os.close(stderr_backup)

        # Release the video capture object
        cap.release()

        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to PIL Image
        pil_image = Image.fromarray(frame_rgb)

        # Apply blur filter with specified radius
        blurred_image = pil_image.filter(ImageFilter.GaussianBlur(blur_radius))

        return blurred_image

    except Exception as e:
        print(f"{RED}[X]{RESET} Error: Processing video file failed {video_path}: {e}")
        return None

# Main function to process video folders
def process_video_files(root_folder, blur_radius, thumb_quality, force):
    # Print "Start" message on process start
    print(f"{GREEN}[>]{RESET} Starting spoiler-free thumbnail generation in {root_folder}...\n")

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith((".mp4", ".mkv", ".avi")):
                video_path = os.path.join(root, file)
                jpg_file_name = os.path.splitext(file)[0] + ".jpg"
                jpg_file_path = os.path.join(root, jpg_file_name)

                # Check if the thumbnail already exists
                if not force and os.path.exists(jpg_file_path):
                    # Print message that generation is skipped because thumbnail already exists
                    print(f"  {CYAN}[i]{RESET} Thumbnail already exists for {file}, skipping...")
                    continue

                # Print message with active thumbnail generation
                print(f"  {YELLOW}[~]{RESET} Creating thumbnail for {file}...")
                blurred_image = process_video(video_path, blur_radius)
                if blurred_image is not None:
                    blurred_image.save(os.path.join(root, jpg_file_name), quality=thumb_quality)
                    print(f"  {GREEN}[+]{RESET} Thumbnail created for {file}")

# Set up argument parser
parser = argparse.ArgumentParser(description="Generate spoiler-free thumbnails for video files.")
parser.add_argument("folder", nargs="?", default=None, help="Path to the folder containing videos.")
parser.add_argument("--force", action="store_true", help="Force thumbnail creation even if they already exist.")
parser.add_argument("--blur_radius", type=int, default=100, help="Set the radius of the blur effect (default: 100).")
parser.add_argument("--thumb_quality", type=int, default=80, help="Set the quality of the thumbnail (default: 80).")
args = parser.parse_args()

# Ask for confirmation if -force is provided
if args.force:
    print(f"\n{YELLOW}[!]{RESET} Warning: Argument -force was set, existing thumbnails will be regenerated...")

    confirmation = input("Are you sure you want to regenerate existing thumbnails? (Y/n): ")
    if confirmation.lower() != 'y':
        print(f"{RED}[X]{RESET} Operation cancelled.")
        exit()

# Args
if args.folder:
    root_folder = args.folder
else:
    warn_root_folder = os.path.dirname(os.path.abspath(__file__))
    print(f"\n{YELLOW}[!]{RESET} Warning: No folder was set, thumbnails will be generated in {warn_root_folder} and all subdirectories.")
    confirmation = input("Are you sure you want to generate thumbnails? (Y/n): ")
    if confirmation.lower() != 'y':
        print(f"{RED}[X]{RESET} Operation cancelled.")
        exit()
    root_folder = warn_root_folder

blur_radius = args.blur_radius
thumb_quality = args.thumb_quality
force = args.force

# Call the function to process video files
process_video_files(root_folder, blur_radius, thumb_quality, force)

# Print "Done" message after processing is complete
print(f"\n{GREEN}[OK]{RESET} Successfully processed all video files. Happy spoiler-free watching! :)")
