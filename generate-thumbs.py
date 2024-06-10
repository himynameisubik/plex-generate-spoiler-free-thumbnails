import os
import random
import cv2
from PIL import Image, ImageFilter

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
        print(f"Error processing video file {video_path}: {e}")
        return None
        
# Main function to process TV show folders
def process_tv_shows(root_folder, blur_radius):
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith((".mp4", ".mkv", ".avi")):
                video_path = os.path.join(root, file)
                blurred_image = process_video(video_path, blur_radius)
                if blurred_image is not None:
                    jpg_file_name = os.path.splitext(file)[0] + ".jpg"
                    blurred_image.save(os.path.join(root, jpg_file_name), quality=thumb_quality)  # Adjust quality level as needed
                    print(f"Blurred image created for {file}")

# Set the root folder
root_folder = os.path.dirname(os.path.abspath(__file__))

# Define the blur radius
blur_radius = 100   # Adjust this value to control the amount of blur

# Define thumbnail quality
thumb_quality = 80  # Adjust this value to control the quality of the thumbnail

# Call the function to process TV show folders
process_tv_shows(root_folder, blur_radius)

# Print "Done" message after processing is complete
print()
print("-- All images processed successfully.")
