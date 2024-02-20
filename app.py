import os
import yt_dlp
import subprocess
import boto3
import urllib.parse
from urllib.parse import urlparse
from flask import Flask, redirect
from flask_cors import CORS, cross_origin
import zipfile
from flask import Flask, render_template, request, jsonify
import json


app = Flask(__name__)
cors = CORS(app)


def upload_file_to_s3(file_name, bucket_name = "quick-translates", object_name=None):
    # Create an S3 client
    s3_client = boto3.client('s3')
    
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    object_name = "whisper_outputs/" + object_name
  
        # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
        print(response)
    except Exception as e:
        print(f"Error uploading file: {e}")

        # Generate the URL to get 'file_name' from S3
    url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"

    return url


def save_as_file(text, filename):

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


@app.route('/', methods=['POST'])
def save_changes_subtitles():
    
    data = json.loads(request.data)
    print(data)
    txt_file_content = data['txt_file_content']
    srt_file_content = data['srt_file_content']
    folder_name = data['folder_name']
    srt_file_name = folder_name + '.srt'
    txt_file_name = folder_name + '.txt'
    zip_file_name = folder_name + '.zip'

     # Base name for the video file
    
    save_as_file(srt_file_content, srt_file_name)
    save_as_file(txt_file_content, txt_file_name)
   
    with zipfile.ZipFile(zip_file_name, 'w') as myzip:
        myzip.write(srt_file_name)
        myzip.write(txt_file_name)
   
    url = upload_file_to_s3(zip_file_name)
    print(url)
    os.remove(srt_file_name)
    os.remove(txt_file_name)
    os.remove(zip_file_name)
    return jsonify({'url': url})


if __name__== '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)

