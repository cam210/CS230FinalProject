import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def trim_video(file_path, start_time, end_time):
    try:
        # Load the video
        with VideoFileClip(file_path, audio=False) as video:
            # Ensure that the video is at least 5 seconds long
            video_duration = video.duration
            if video_duration < end_time:
                end_time = video_duration  # Trim up to the video's actual duration if it's shorter
            
            # Trim the video from start_time to end_time
            trimmed_video = video.subclip(start_time, end_time)
            
            # Overwrite the original video with the trimmed one
            output_path = file_path.replace(".mp4", "_trimmed.mp4")  # Temporary file
            trimmed_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
            
            # Replace original video with the trimmed version
            os.replace(output_path, file_path)
        
        print(f"Successfully trimmed and replaced: {file_path}")
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def trim_all_videos_in_folder(folder_path, start_time=0, end_time=5):
    total_files = 0
    trimmed_files = 0
    
    # Loop through all files in the specified folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Check if the file is a video (you can extend this to check for other formats)
        if file_name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv')):
            total_files += 1
            if trim_video(file_path, start_time, end_time):
                trimmed_files += 1
            print(f"Trimmed {trimmed_files} out of {total_files} videos so far.")
    
    print(f"Final tally: Trimmed {trimmed_files} out of {total_files} videos.")

if __name__ == "__main__":
    # Define the folder containing the videos
    folder_path = "/Users/cameronburton/Desktop/CS230_Final_Project/Chris_Sale/Healthy"
    
    # Call the function to trim all videos in the folder to the first 5 seconds
    trim_all_videos_in_folder(folder_path)