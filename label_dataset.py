import os
import pandas as pd

def create_annotations_csv(dataset_dir, output_csv):
    data = []
    
    # Define label mapping
    labels = {"healthy": 0, "injured": 1}
    
    # Traverse through the 'healthy' and 'injured' directories
    for label_name, label_value in labels.items():
        label_dir = os.path.join(dataset_dir, label_name)
        for video_file in os.listdir(label_dir):
            if video_file.endswith('.mp4'):
                video_path = os.path.join(label_dir, video_file)
                data.append([video_path, label_value])
    
    # Create a DataFrame and save it as a CSV
    df = pd.DataFrame(data, columns=["filepath", "label"])
    df.to_csv(output_csv, index=False)
    print(f"Annotation CSV created at {output_csv}")

# Path to your dataset directory and desired CSV output path
dataset_dir = '/Users/cameronburton/Desktop/CS230_Final_Project/Final_Dataset'
output_csv = os.path.join(dataset_dir, 'annotations.csv')

# Create the annotation CSV
create_annotations_csv(dataset_dir, output_csv)