import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm  # Import tqdm for progress tracking

# Parameters for preprocessing
TARGET_FRAME_COUNT = 16  # Number of frames per video
FRAME_SIZE = (64, 64)    # Width and height of each frame

def preprocess_video(video_path, target_frames=TARGET_FRAME_COUNT, frame_size=FRAME_SIZE):
    # Attempt to open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return None

    frames = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        print(f"Warning: Video {video_path} contains no frames.")
        cap.release()
        return None

    # Calculate the sampling interval
    sampling_interval = max(1, total_frames // target_frames)
    frame_count = 0

    # Process frames
    while cap.isOpened() and len(frames) < target_frames:
        ret, frame = cap.read()
        if not ret:
            print(f"Warning: Could not read frame {frame_count} in video {video_path}.")
            break

        # Only process every `sampling_interval` frame
        if frame_count % sampling_interval == 0:
            try:
                # Resize frame to target dimensions
                frame = cv2.resize(frame, frame_size)
                frames.append(frame)
            except Exception as e:
                print(f"Error resizing frame {frame_count} in video {video_path}: {e}")
                cap.release()
                return None

        frame_count += 1

    cap.release()

    # If no frames were captured, return None
    if not frames:
        print(f"Warning: No frames captured from video {video_path}")
        return None

    # If there are fewer frames than target_frames, repeat the last frame
    while len(frames) < target_frames:
        frames.append(frames[-1])  # Safely repeat last frame only if frames list is not empty

    # Convert list of frames to a numpy array
    video_array = np.array(frames)
    return video_array

# Function to load dataset from CSV with progress tracking
def load_videos_from_csv(csv_path):
    data = pd.read_csv(csv_path)
    videos = []
    labels = []
    
    # Use tqdm to display progress
    for _, row in tqdm(data.iterrows(), total=data.shape[0], desc="Processing videos"):
        video_path = row['filepath']
        label = row['label']
        
        # Preprocess the video
        video_array = preprocess_video(video_path)
        
        # Only append if preprocessing was successful
        if video_array is not None:
            videos.append(video_array)
            labels.append(label)
        else:
            print(f"Skipping video {video_path} due to preprocessing error.")
    
    # Convert lists to numpy arrays
    videos = np.array(videos)
    labels = np.array(labels)
    return videos, labels

# Example usage with training set
train_videos, train_labels = load_videos_from_csv('/Users/cameronburton/Desktop/CS230_Final_Project/Final_Dataset/train.csv')