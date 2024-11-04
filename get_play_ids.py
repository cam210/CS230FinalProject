import os
import pandas as pd
import requests
import lxml.html
import io
from tqdm import tqdm

# Function to fetch video URL using the play_id
def fetch_video_url(play_id):
    try:
        # Fetch the page with the play_id
        response = requests.get(f'https://baseballsavant.mlb.com/sporty-videos?playId={play_id}')
        tree = lxml.html.fromstring(response.text)
        video_url = tree.xpath('//video[@id="sporty"]/source/@src')

        if not video_url:
            raise ValueError(f"No video URL found for play_id: {play_id}")

        return video_url[0]
    except Exception as e:
        print(f"Error fetching video URL for play_id {play_id}: {e}")
        return None

# Function to download video from the fetched URL
def download_video(video_url, save_path):
    try:
        # Stream the video content and download in chunks
        response = requests.get(video_url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))

        # Write video content to the specified file path
        with open(save_path, 'wb') as f:
            for data in tqdm(response.iter_content(1024), total=total_size // 1024, unit='KB'):
                f.write(data)
        print(f"Downloaded {save_path}")
        return True
    except Exception as e:
        print(f"Failed to download video from {video_url}: {e}")
        return False

# Function to process the play_ids from the Excel file and download videos
def download_videos_from_excel(excel_file, save_directory, url_column='URL'):
    # Load the Excel sheet
    df = pd.read_excel(excel_file)

    # Check if the save directory exists, if not, create it
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Iterate through each row and extract play_id
    for index, row in df.iterrows():
        url = row[url_column]
        # Extract play_id, assuming the URL is in the format "...?playId=<play_id>"
        play_id = url.split('=')[-1]

        # Fetch video URL using the play_id
        video_url = fetch_video_url(play_id)

        if video_url:
            video_name = f"play_{play_id}.mp4"
            save_path = os.path.join(save_directory, video_name)

            # Download the video
            download_video(video_url, save_path)

if __name__ == "__main__":
    # Path to the Excel file and save directory
    excel_file_path = "/Users/cameronburton/Desktop/CS230_Final_Project/Walker_Buehler/Walker_Buehler_Healthy.xlsx"
    save_directory = "/Users/cameronburton/Desktop/CS230_Final_Project/Walker_Buehler/Healthy"

    # Download videos from the play_ids in the Excel file
    download_videos_from_excel(excel_file_path, save_directory)
