import os
import argparse
from PIL import Image, ImageFilter
import ffmpeg
import numpy as np

# Colors
RED = "\033[31m"
GREEN = "\033[92m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RESET = "\033[0m"

def is_mostly_black(frame, threshold=0.95, dark_threshold=20, debug=False):
    # Check if the frame is mostly black or very dark, returns True if the frame is considered black/dark.

    # Convert to grayscale for easier processing
    gray = np.mean(frame, axis=2)
    
    # Calculate average brightness (0-255)
    avg_brightness = np.mean(gray)
    
    # Check percentage of very dark pixels
    dark_pixels = np.sum(gray < dark_threshold)
    total_pixels = gray.size
    dark_ratio = dark_pixels / total_pixels
    
    if debug:
        print(f"    Debug: avg_brightness={avg_brightness:.2f}, dark_ratio={dark_ratio:.2%}, threshold={threshold:.2%}")
    
    # If more than threshold% of pixels are dark, consider it black
    return dark_ratio > threshold

def extract_non_black_frame(video_path, debug=False):
    try:
        # Get video info using ffmpeg
        probe = ffmpeg.probe(video_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        
        if video_stream is None:
            raise Exception("No video stream found")
        
        # Get duration and fps
        duration = float(video_stream.get('duration', 0))
        if duration == 0:
            duration = float(probe.get('format', {}).get('duration', 0))
        
        fps = eval(video_stream.get('r_frame_rate', '0/1'))
        
        # Calculate middle timestamp
        middle_timestamp = duration / 2
        
        if debug:
            print(f"    Debug: Duration: {duration:.2f}s, FPS: {fps}, Middle timestamp: {middle_timestamp:.2f}s")
        
        # Try timestamps around the middle (±10 seconds or ±10 frames, whichever is larger)
        # Let's try 20 timestamps around the middle
        timestamps_to_try = []
        
        # Add timestamps around the middle (20 timestamps)
        for i in range(-10, 11):
            # Adjust by 0.5 seconds each step, but don't go beyond boundaries
            offset = i * 0.5
            ts = middle_timestamp + offset
            if 0 <= ts <= duration:
                timestamps_to_try.append(ts)
        
        for timestamp in timestamps_to_try:
            if debug:
                print(f"    Checking timestamp {timestamp:.2f}s...")
            
            # Extract frame
            try:
                out, err = (
                    ffmpeg
                    .input(video_path, ss=timestamp)
                    .output('pipe:', format='rawvideo', pix_fmt='rgb24', vframes=1)
                    .run(capture_stdout=True, capture_stderr=True, quiet=True)
                )
                
                # Get video dimensions
                width = int(video_stream['width'])
                height = int(video_stream['height'])
                
                # Convert to numpy array
                frame = np.frombuffer(out, np.uint8).reshape([height, width, 3])
                
                # Check if frame is not mostly black
                if not is_mostly_black(frame, debug=debug):
                    if debug:
                        print(f"    Found good frame at timestamp {timestamp:.2f}s")
                    return frame
                elif debug:
                    print(f"    Frame at {timestamp:.2f}s is too dark, skipping...")
                    
            except ffmpeg.Error as e:
                if debug:
                    print(f"    Error extracting frame at {timestamp:.2f}s: {e}")
                continue
        
        # If all frames are black, just return the middle frame
        if debug:
            print(f"  {YELLOW}[!]{RESET} Could not find non-black frame, using middle frame anyway")
        
        out, err = (
            ffmpeg
            .input(video_path, ss=middle_timestamp)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24', vframes=1)
            .run(capture_stdout=True, capture_stderr=True, quiet=True)
        )
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        return np.frombuffer(out, np.uint8).reshape([height, width, 3])
        
    except Exception as e:
        print(f"{RED}[X]{RESET} Error extracting frame from {video_path}: {e}")
        return None

# Function to process video files and create blurred images
def process_video(video_path, blur_radius, debug=False):
    try:
        # Extract non-black frame
        frame = extract_non_black_frame(video_path, debug=debug)
        
        if frame is None:
            return None
        
        # Convert to PIL Image
        pil_image = Image.fromarray(frame)
        
        # Apply blur filter with specified radius
        blurred_image = pil_image.filter(ImageFilter.GaussianBlur(blur_radius))
        
        return blurred_image
        
    except Exception as e:
        print(f"{RED}[X]{RESET} Error: Processing video file failed {video_path}: {e}")
        return None

# Main function to process video folders
def process_video_files(root_folder, blur_radius, thumb_quality, force, debug):
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
                    print(f"  {CYAN}[i]{RESET} Thumbnail already exists for {file}, skipping...")
                    continue

                # Print message with active thumbnail generation
                print(f"  {YELLOW}[~]{RESET} Creating thumbnail for {file}...")
                blurred_image = process_video(video_path, blur_radius, debug=debug)
                if blurred_image is not None:
                    blurred_image.save(os.path.join(root, jpg_file_name), quality=thumb_quality)
                    print(f"  {GREEN}[+]{RESET} Thumbnail created for {file}")

# Set up argument parser
parser = argparse.ArgumentParser(description="Generate spoiler-free thumbnails for video files.")
parser.add_argument("folder", nargs="?", default=None, help="Path to the folder containing videos.")
parser.add_argument("--force", action="store_true", help="Force thumbnail creation even if they already exist.")
parser.add_argument("--blur_radius", type=int, default=100, help="Set the radius of the blur effect (default: 100).")
parser.add_argument("--thumb_quality", type=int, default=80, help="Set the quality of the thumbnail (default: 80).")
parser.add_argument("--debug", action="store_true", help="Enable debug output for frame analysis")
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
    warn_root_folder = os.getcwd()
    print(f"\n{YELLOW}[!]{RESET} Warning: No folder was set, thumbnails will be generated in {warn_root_folder} and all subdirectories.")
    confirmation = input("Are you sure you want to generate thumbnails? (Y/n): ")
    if confirmation.lower() != 'y':
        print(f"{RED}[X]{RESET} Operation cancelled.")
        exit()
    root_folder = warn_root_folder

blur_radius = args.blur_radius
thumb_quality = args.thumb_quality
force = args.force
debug = args.debug

# Call the function to process video files
process_video_files(root_folder, blur_radius, thumb_quality, force, debug)

# Print "Done" message after processing is complete
print(f"\n{GREEN}[OK]{RESET} Successfully processed all video files. Happy spoiler-free watching! :)")