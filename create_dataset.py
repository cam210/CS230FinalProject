import cv2
import mediapipe as mp
import pandas as pd
import os

# Initialize MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Function to process each video and extract pose keypoints
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    keypoints_data = []

    # Loop through frames in the video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the image color to RGB (MediaPipe uses RGB)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        # Extract keypoints if any are detected
        if results.pose_landmarks:
            frame_keypoints = []
            for landmark in results.pose_landmarks.landmark:
                frame_keypoints.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])

            # Append keypoints for the frame
            keypoints_data.append(frame_keypoints)

    cap.release()
    return keypoints_data

# Process all videos in a specified directory
def process_videos_in_directory(directory_path):
    all_data = []  # List to store all keypoints data across videos
    video_files = [f for f in os.listdir(directory_path) if f.endswith('.mp4')]  # Assuming videos are in .mp4 format

    for video_file in video_files:
        video_path = os.path.join(directory_path, video_file)
        video_keypoints = process_video(video_path)

        # Convert the list of keypoints into a DataFrame for this video
        video_df = pd.DataFrame(video_keypoints, columns=[f"{j}_{coord}" for j in range(33) for coord in ["x", "y", "z", "visibility"]])
        video_df["video_name"] = video_file  # Add a column for the video name

        # Append to the main list
        all_data.append(video_df)

    # Concatenate all DataFrames into a single DataFrame
    result_df = pd.concat(all_data, ignore_index=True)
    return result_df

# Path to directory with trimmed videos
directory_path = '/Users/cameronburton/Desktop/CS230_Final_Project/Walker_Buehler/Test'
pose_data_df = process_videos_in_directory(directory_path)

# Output the DataFrame as input for a neural network
print(pose_data_df)
pose_data_df.to_csv('pose_keypoints_data.csv', index=False)

output_path = os.path.join(directory_path, 'pose_keypoints_data.csv')
pose_data_df.to_csv(output_path, index=False)
print(f"Data saved to {output_path}")