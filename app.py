import os
import yt_dlp
import subprocess
import boto3
import urllib.parse
from urllib.parse import urlparse
from flask import Flask, redirect
from flask_cors import CORS, cross_origin

from flask import Flask, render_template, request, jsonify
import json


app = Flask(__name__)
cors = CORS(app)


def save_as_srt(text, filename):
    """Saves the given text as an SRT file with appropriate formatting.

    Args:
        text (str): The text to be saved, divided into subtitle lines with
                  timestamps in the SRT format (e.g., "00:00:00,000 --> 00:00:03,480").
        filename (str): The desired filename for the SRT file.

    Raises:
        ValueError: If the text does not contain valid SRT entries.
    """

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


def upload_video_to_s3(file_name, bucket_name = "quick-translates", object_name=None):
    # Create an S3 client
    s3_client = boto3.client('s3')
    
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    object_name = "burned_video/" + object_name
  
        # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
        print(response)
    except Exception as e:
        print(f"Error uploading file: {e}")

        # Generate the URL to get 'file_name' from S3
    url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"

    return url

def download_video_from_s3(url, input_video_file_path):
    command = f'curl -o {input_video_file_path} "{url}"'
    subprocess.run(command, shell=True, check=True)

@app.route('/', methods=['POST'])
def download_video():
    
    data = json.loads(request.data)
    print(data)
    video_link = data['video_link']
    srt_file_content = data['srt_file_content']
    s3_youtube_flag = data['s3_youtube_flag']

    video_folder_path = os.getcwd()
    file_name = str(video_link)[-5:] 
    input_video_file_path = os.path.join(video_folder_path, file_name + '.mp4')
    
     # Base name for the video file
    
    output_file = file_name + 'output_file'  # Current working directory
    save_as_srt(srt_file_content, 'srt_file_download.srt')
    srt_file = 'srt_file_download.srt'
        # Ensuring the video folder path exists
        # Full path for the downloaded video file
       
       
          # Assuming mp4 format
    if s3_youtube_flag == "youtube":
        # yt-dlp options for downloading video
        ytdl_opts = {
            'outtmpl': input_video_file_path ,  # Use the original file extension
            #'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Prioritize MP4 format
            'format': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best'
        }

        # Downloading the video
        ytdl = yt_dlp.YoutubeDL(ytdl_opts)

        # Now you can use ytdl to download a video. For example:
        ytdl.download(video_link)

        # Constructing FFmpeg command for adding subtitles
    if s3_youtube_flag == "s3":
        download_video_from_s3(video_link, input_video_file_path)
    else:
        print("Invalid flag")
    output_video_file_path = os.path.join(video_folder_path, output_file + '.mp4')

    ffmpeg_command = [
            'ffmpeg',
            '-i', input_video_file_path,  # Input video file path
            '-vf', f'subtitles={srt_file}',
            output_video_file_path  # Output video file path
        ]

        # Running the FFmpeg command
    subprocess.run(ffmpeg_command)
    s3_file_path_burned_video = upload_video_to_s3(output_video_file_path)
    os.remove(output_video_file_path)
    os.remove(input_video_file_path)

    return {'s3_burned_video_file_path':s3_file_path_burned_video}

if __name__== '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)

