import os
import yt_dlp
import subprocess
import boto3
import urllib.parse
from urllib.parse import urlparse
from flask import Flask, redirect
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
import json

## Live Key 
## test Key 
#stripe.api_key = 'sk_test_51McuMBLJQCcJOmwnJbqPeQqk3PshBcYrfqybQZKAS0D5gy8uZGI8X7FMsj6e0iTZenWiU7kcTYx6bDCMpTXuU5hu007jfHB3Iw'

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://app.quicktranslates.com",
                "https://app-staging-quicktranslates.netlify.app",
                "http://localhost:8080"
            ],
            "expose_headers": "Access-Control-Request-Headers",  # Add this line
            "allow_headers": "Content-Type",  # Specify allowed headers
        }
    }
)


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
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Prioritize MP4 format
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

    return s3_file_path_burned_video

if __name__== '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)




# srt_content = """

# 1
# 00:00:00,000 --> 00:00:03,480
# The construction of a new Ramayana temple in Ayodhya is being completed.

# 2
# 00:00:03,480 --> 00:00:08,560
# The life restoration of this temple is going to be completed on the 22nd of this month.

# 3
# 00:00:08,560 --> 00:00:11,320
# Now in this place where the Ramayana temple stands,

# 4
# 00:00:11,320 --> 00:00:15,800
# 500 years ago, in fact, in AD 1528,

# 5
# 00:00:15,800 --> 00:00:19,800
# The construction of a Muslim temple called Babri Masjid had been completed.

# 6
# 00:00:19,800 --> 00:00:25,240
# So the history of Babri Masjid and the 500-year history of the Ramayana temple

# 7
# 00:00:25,240 --> 00:00:27,520
# Not only the history of these two temples,

# 8
# 00:00:27,520 --> 00:00:32,960
# We can see that it is also a large segment of India's social, cultural, and national history.

# 9
# 00:00:32,960 --> 00:00:37,520
# So that history is the 500-year history of that dispute related to Ayodhya.

# 10
# 00:00:37,520 --> 00:00:40,320
# Looking forward to today's video, let's move on to the video.

# 11
# 00:00:40,320 --> 00:00:43,520
# My name is Alex. What I do is explain. Welcome to Alex Plain.

# 12
# 00:00:51,520 --> 00:00:55,800
# So it is said that Babri Masjid was built in 1528.

# 13
# 00:00:55,800 --> 00:01:01,120
# If you go back two more years, it is in 1526 that the First Panipat War took place.

# 14
# 00:01:01,120 --> 00:01:05,920
# In this war, Babar defeated the sultanate king named Ibrahim Lodhi

# 15
# 00:01:05,920 --> 00:01:09,120
# It was the beginning of the Mughal dynasty in India.

# 16
# 00:01:09,120 --> 00:01:11,800
# So the commander of Babar was called Mir Bakki.

# 17
# 00:01:11,800 --> 00:01:18,600
# It was Mir Bakki who established a Muslim temple here in 1528 and dedicated it to Babar.

# 18
# 00:01:18,600 --> 00:01:22,480
# But this history can be seen after a long time.

# 19
# 00:01:22,480 --> 00:01:27,280
# So Babar's biography or biography is the book called Babar Nama.

# 20
# 00:01:27,280 --> 00:01:32,680
# There is nothing in this book about such a temple or Babri Masjid.

# 21
# 00:01:32,680 --> 00:01:37,280
# The first thing we see about this building or this mosque is

# 22
# 00:01:37,280 --> 00:01:43,080
# It is from the works of Jai Singh II, who was a Rajput representative of this Mughal palace.

# 23
# 00:01:43,080 --> 00:01:45,480
# He is called Sawai Jai Singh.

# 24
# 00:01:45,480 --> 00:01:51,080
# So he purchased some of the prominent places for Hindus in all these areas.

# 25
# 00:01:51,280 --> 00:01:57,480
# In such places, this Sawai Jai Singh was providing facilities for Hindus to conduct worship.

# 26
# 00:01:57,480 --> 00:02:03,280
# So in such places, a sketch of a building with three pillars can be seen in his drawings.

# 27
# 00:02:03,280 --> 00:02:08,280
# So he says that the courtyard around that building is the only place for Hindus to pray.

# 28
# 00:02:08,280 --> 00:02:11,080
# He refers to that place as Janmasthan.

# 29
# 00:02:11,080 --> 00:02:16,680
# So it is thought that the sketch in his drawings is from this Babri Masjid.

# 30
# 00:02:16,680 --> 00:02:20,280
# But even then, it was not possible to find a connection with Babar.

# 31
# 00:02:20,280 --> 00:02:24,280
# It happens after the 17th century British invaders came to India.

# 32
# 00:02:24,280 --> 00:02:30,680
# The British surveyor named Francis Buchanan later entered this mosque and found some inscriptions there.

# 33
# 00:02:30,680 --> 00:02:36,280
# So in one inscription, he will find the inscription that says this mosque is dedicated to Babar.

# 34
# 00:02:36,280 --> 00:02:38,680
# Establish that connection with Babar.

# 35
# 00:02:38,680 --> 00:02:42,680
# That is how this mosque was later known as Babri Masjid.

# 36
# 00:02:42,680 --> 00:02:46,280
# However, the place called Ayodhya, where this Babri Masjid is located,

# 37
# 00:02:46,280 --> 00:02:50,680
# It is a place of great importance in connection with Hinduism.

# 38
# 00:02:50,680 --> 00:02:56,280
# It is believed that this Ayodhya is the birthplace of Sri Rama, the seventh incarnation of Mahavishnu.

# 39
# 00:02:56,280 --> 00:03:04,680
# Not only that, there is a great belief that the place called Ayodhya has been passed down from generation to generation among Hinduism.

# 40
# 00:03:04,680 --> 00:03:09,280
# There used to be a Rama temple in the birthplace of Sri Rama.

# 41
# 00:03:09,280 --> 00:03:17,280
# It is believed that Babar's commander, Babri Masjid Panitha, destroyed this Rama temple.

# 42
# 00:03:17,280 --> 00:03:22,280
# Not only that, there is a courtyard around the place called Babri Masjid Mosque.

# 43
# 00:03:22,280 --> 00:03:28,280
# In that courtyard, we can see some elevated platforms such as Ram Chabutra and Sita Rasoi.

# 44
# 00:03:28,280 --> 00:03:32,280
# On those platforms, they believe that Ram Chabutra is the birthplace of Ram.

# 45
# 00:03:32,280 --> 00:03:37,280
# Hindu religious believers used to pray in various ways from time to time.

# 46
# 00:03:37,280 --> 00:03:44,280
# Since there is such a belief among the people that the Rama temple was destroyed and a mosque was built there,

# 47
# 00:03:44,280 --> 00:03:53,280
# There used to be some minor problems between people who believed in both Hinduism and Islam in the place called Ayodhya.

# 48
# 00:03:53,280 --> 00:03:59,280
# But there is a big problem between the beliefs of these two religions in 1855.

# 49
# 00:03:59,280 --> 00:04:03,280
# If we look at that time, we can see that the British were occupying India.

# 50
# 00:04:04,280 --> 00:04:11,280
# So that this problem does not escalate further and such problems do not arise in the future, the British are taking a lead here.

# 51
# 00:04:11,280 --> 00:04:18,280
# In this place, this mosque and the courtyard around it are located in 2.77 acres.

# 52
# 00:04:18,280 --> 00:04:20,280
# Here they are building a railing.

# 53
# 00:04:20,280 --> 00:04:24,280
# Babri Masjid and this courtyard are separated by such a railing.

# 54
# 00:04:24,280 --> 00:04:29,280
# As part of that, Hindus can pray in this courtyard.

# 55
# 00:04:29,280 --> 00:04:32,280
# Muslims can use this mosque for their Namaz.

# 56
# 00:04:32,280 --> 00:04:35,280
# This is how things are moving forward.

# 57
# 00:04:35,280 --> 00:04:39,280
# Then a major development comes here in 1885.

# 58
# 00:04:39,280 --> 00:04:46,280
# Mahanthi Raghupir Das, who was in charge of the mosque's courtyard, is approaching the court.

# 59
# 00:04:46,280 --> 00:04:55,280
# He is filing a case to move their worship forward around a platform called Ram Chabutra.

# 60
# 00:04:55,280 --> 00:04:59,280
# This case was heard in three different levels of courts.

# 61
# 00:04:59,280 --> 00:05:02,280
# Each court is said to maintain the status quo.

# 62
# 00:05:02,280 --> 00:05:04,280
# So how are things moving forward now?

# 63
# 00:05:04,280 --> 00:05:06,280
# It is said to move forward in the same way.

# 64
# 00:05:06,280 --> 00:05:10,280
# Later, until India gains independence, major developments do not take place in this place.

# 65
# 00:05:10,280 --> 00:05:12,280
# India gained independence in 1947.

# 66
# 00:05:12,280 --> 00:05:19,280
# But in 1949, there was a very important incident related to this Ayodhya issue.

# 67
# 00:05:19,280 --> 00:05:29,280
# A Hindu organization called Akhila Parathiya Ramayana Mahasabha organizes a parayana program of Ram Charita Manas, which lasts for nine days.

# 68
# 00:05:29,280 --> 00:05:31,280
# This event takes place on December 49.

# 69
# 00:05:31,280 --> 00:05:34,280
# The last day of this is December 22.

# 70
# 00:05:34,280 --> 00:05:39,280
# After this event, some people enter this mosque at night.

# 71
# 00:05:39,280 --> 00:05:42,280
# There are three lower courtyards in the middle of the mosque.

# 72
# 00:05:42,280 --> 00:05:48,280
# Under the lower courtyard in the middle, statues of Rama, Sita and Lakshmana are erected.

# 73
# 00:05:48,280 --> 00:05:54,280
# So even though they are doing this, this news is spreading among the Hindu community in Ayodhya and beyond.

# 74
# 00:05:54,280 --> 00:05:58,280
# Mysteriously, the statues of Rama have appeared in this mosque.

# 75
# 00:05:58,280 --> 00:06:02,280
# That is why a new belief is spreading among people.

# 76
# 00:06:02,280 --> 00:06:03,280
# It is not Ram Chabutra.

# 77
# 00:06:03,280 --> 00:06:07,280
# The birthplace of Sri Rama is actually under the main lower courtyard of this mosque.

# 78
# 00:06:07,280 --> 00:06:11,280
# That is why the news that these statues have appeared there is spreading like wildfire.

# 79
# 00:06:11,280 --> 00:06:17,280
# Many people from all over the world come to Ayodhya to see this scene and pray.

# 80
# 00:06:17,280 --> 00:06:21,280
# The government has announced that there may be major problems here.

# 81
# 00:06:21,280 --> 00:06:25,280
# The Prime Minister of that time, Sri Jawaharlal Nehru, as well as Sardar Vallabh Bhai Patel,

# 82
# 00:06:25,280 --> 00:06:29,280
# and the Chief Minister of the UP government, Sri Govind Vallabh,

# 83
# 00:06:29,280 --> 00:06:35,280
# are looking forward to removing these statues from this mosque as soon as possible.

# 84
# 00:06:35,280 --> 00:06:41,280
# The Chief Minister of that time is coming to the district commission of that time, in the district called Faisabad.

# 85
# 00:06:41,280 --> 00:06:44,280
# He is talking to KK Nair, who was the district commission of that time.

# 86
# 00:06:44,280 --> 00:06:56,280
# The reply he gives is that these statues can be successfully removed from there, but if so, there is a possibility that there will be a great chaos here and peace will not be restored.

# 87
# 00:06:56,280 --> 00:07:00,280
# He decides not to remove these statues from the mosque.

# 88
# 00:07:00,280 --> 00:07:03,280
# But by then the situation was getting out of hand.

# 89
# 00:07:03,280 --> 00:07:16,280
# That is why the government has decided to close the doors of the mosque and hand over all the control of these premises to a government receiver.

# 90
# 00:07:16,280 --> 00:07:22,280
# So this incident in 1941 is very important because of two important things.

# 91
# 00:07:22,280 --> 00:07:27,280
# First, for a long time people believed that Ram's birthplace was Ram's son.

# 92
# 00:07:27,280 --> 00:07:30,280
# People had put forward the idea that a temple should be built there.

# 93
# 00:07:30,280 --> 00:07:37,280
# But after this incident, people believe that Ram's birthplace is below the main mosque.

# 94
# 00:07:37,280 --> 00:07:40,280
# A desire to build a temple there is being put forward.

# 95
# 00:07:40,280 --> 00:07:44,280
# The second thing is that after this incident, the mosque was never opened again.

# 96
# 00:07:44,280 --> 00:07:47,280
# The mosque was closed and closed with that incident.

# 97
# 00:07:47,280 --> 00:07:52,280
# That is why this incident in 1941 is very important.

# 98
# 00:07:52,280 --> 00:08:00,280
# After this incident, many people will come forward with the right to this disputed land of 2.77 acres.

# 99
# 00:08:00,280 --> 00:08:02,280
# We can see that they are carrying out cases.

# 100
# 00:08:02,280 --> 00:08:07,280
# Among them, the most important is the Nirmohi Akhara, which came forward in 1959.

# 101
# 00:08:07,280 --> 00:08:18,280
# Nirmohi Akhara is a group of people who look after the temples and other things related to Sri Ram in North India.

# 102
# 00:08:18,280 --> 00:08:25,280
# Since this is also a matter related to Sri Ram, it is a claim to see the full right of this land.

# 103
# 00:08:25,280 --> 00:08:27,280
# Nirmohi Akhara is going forward.

# 104
# 00:08:27,280 --> 00:08:34,280
# That is why in 1961, the Sunni Waqf Board of Uttar Pradesh came forward by representing Muslims.

# 105
# 00:08:35,280 --> 00:08:40,280
# The Waqf Board is a group of people who look after the temples and other things related to the Muslim religion.

# 106
# 00:08:40,280 --> 00:08:42,280
# The control of this whole area is yours.

# 107
# 00:08:42,280 --> 00:08:46,280
# Since there is a mosque there, it is necessary for you to have the right.

# 108
# 00:08:46,280 --> 00:08:48,280
# That is why they cornered and filed a case.

# 109
# 00:08:48,280 --> 00:08:56,280
# Around the same time, a new movement is being used by other major Hindu organizations of the World Hindu Exhibition.

# 110
# 00:08:56,280 --> 00:08:59,280
# The name of this movement was Sri Rama Janmabhoomi Movement.

# 111
# 00:08:59,280 --> 00:09:04,280
# Sri LK Adhwani, who was the leader of the BJP and other Hindu organizations at that time, was the president of this movement.

# 112
# 00:09:04,280 --> 00:09:10,280
# Their most important need was to get that Ram Janmabhoomi or the whole area that is disputed.

# 113
# 00:09:10,280 --> 00:09:13,280
# It was their need to build a temple there.

# 114
# 00:09:13,280 --> 00:09:17,280
# In this way, the debates related to this issue are moving forward.

# 115
# 00:09:17,280 --> 00:09:27,280
# This is how the Shah Banu case, which is a very important event in the history of Indian politics in 1986, and the court ruling against it came forward.

# 116
# 00:09:27,280 --> 00:09:30,280
# What do you think is the connection with this Ayodhya issue?

# 117
# 00:09:30,280 --> 00:09:33,280
# I am not going into the complete details of the Shah Banu case.

# 118
# 00:09:33,280 --> 00:09:41,280
# If you ask what happened here, a Muslim woman is asking for her husband's life after divorcing him and filing a case in the court.

# 119
# 00:09:41,280 --> 00:09:47,280
# So the court's decision at that time was a decision against the Shariah law between Muslims.

# 120
# 00:09:47,280 --> 00:09:50,280
# That is why many Muslim organizations are moving forward with problems.

# 121
# 00:09:51,280 --> 00:10:00,280
# So here, the Rajiv Gandhi government is passing a law that goes against this court ruling, and they are also moving forward.

# 122
# 00:10:00,280 --> 00:10:05,280
# Many Hindu organizations in India are moving forward against this move of the Rajiv Gandhi government.

# 123
# 00:10:05,280 --> 00:10:10,280
# Not only that, the Rajiv Gandhi government is also putting forward allegations that it is a pro-Muslim government.

# 124
# 00:10:10,280 --> 00:10:18,280
# At about the same time, that is, in February 1986, a new case is coming in the Faisabad court in Ayodhya.

# 125
# 00:10:18,280 --> 00:10:24,280
# So it was necessary for Hindus to have a chance to pray there by opening the locks of this mosque.

# 126
# 00:10:24,280 --> 00:10:26,280
# This case was put forward by people.

# 127
# 00:10:26,280 --> 00:10:32,280
# Very surprisingly, the Faisabad district judge in that case is saying a similar law.

# 128
# 00:10:32,280 --> 00:10:39,280
# That is, since that day, Hindus have been allowed to pray and do things there by opening this mosque.

# 129
# 00:10:39,280 --> 00:10:41,280
# This district judge put it forward.

# 130
# 00:10:41,280 --> 00:10:50,280
# So what he is saying is that this decision was put forward as a balancing act against the allegations that the Rajiv Gandhi government was putting forward as part of the Shabanu case.

# 131
# 00:10:50,280 --> 00:10:59,280
# Whether it is right or wrong, we can see that the problems are getting worse again as part of this law by the Faisabad district judge in 1986.

# 132
# 00:10:59,280 --> 00:11:06,280
# In the name of the Babri Masjid Action Committee, Muslims are also moving forward with some of their moments as part of such developments.

# 133
# 00:11:07,280 --> 00:11:13,280
# At this time, in 1989, a very important third party is also moving forward in this case.

# 134
# 00:11:13,280 --> 00:11:15,280
# That is, Ram Lalla Virajman.

# 135
# 00:11:15,280 --> 00:11:18,280
# This Ram Lalla Virajman is Lord Ram.

# 136
# 00:11:18,280 --> 00:11:26,280
# That is, Sri Ram Lalla, the deity of this Ram temple, is moving forward as a part of this case or as a part of this case.

# 137
# 00:11:26,280 --> 00:11:31,280
# Now everyone is wondering how a Hindu god can move forward as a part of a case.

# 138
# 00:11:32,280 --> 00:11:42,280
# Hindu deities, especially Hindu idols, get the status of a juristic person as part of India's legal system.

# 139
# 00:11:42,280 --> 00:11:48,280
# A juristic person is not a real human being, but in the eyes of the law, they are also considered as an ordinary human being.

# 140
# 00:11:48,280 --> 00:11:50,280
# That is what is called a juristic person.

# 141
# 00:11:50,280 --> 00:11:57,280
# So in 1989, in the name of Ram Lalla Virajman, Lord Ram himself is moving forward as a party in this case.

# 142
# 00:11:57,280 --> 00:12:00,280
# Many people are moving forward because he is represented.

# 143
# 00:12:00,280 --> 00:12:05,280
# So, in this way, this case grew and more parties moved forward in it.

# 144
# 00:12:05,280 --> 00:12:16,280
# In August 1989, the Allahabad High Court transferred all the cases related to Ayodhya to the High Court and declared it a land dispute.

# 145
# 00:12:16,280 --> 00:12:22,280
# So, mainly Nirmohi Akhara, as well as the Sunni Worker's Board of Uttar Pradesh, Ram Lalla Virajman,

# 146
# 00:12:22,280 --> 00:12:28,280
# Among these three people, it is a case that determines who has the real right to this land.

# 147
# 00:12:28,280 --> 00:12:35,280
# At this time, another decision by the Indian government to make this matter more complicated is also coming forward.

# 148
# 00:12:35,280 --> 00:12:43,280
# In the face of the Vishwa Hindu trial, right next to this disputed area, the government is giving permission to hold a ceremony called Shila Nayana.

# 149
# 00:12:43,280 --> 00:12:47,280
# Shila Nayana is the foundation stone for the new Ram Temple.

# 150
# 00:12:47,280 --> 00:12:51,280
# The Indian government is giving permission to hold the Shila Establishment.

# 151
# 00:12:51,280 --> 00:12:56,280
# After this, the next important episode in this Ayodhya matter is coming forward.

# 152
# 00:12:56,280 --> 00:13:01,280
# In 1990, at the time of LK Advani, who was the leader of the BJP,

# 153
# 00:13:01,280 --> 00:13:08,280
# From Somanath in Gujarat to Ayodhya in Uttar Pradesh, they are organizing a program called Ratha Yatra.

# 154
# 00:13:08,280 --> 00:13:13,280
# So, if you ask what is the purpose of this Ratha Yatra, which starts in September and ends in October,

# 155
# 00:13:13,280 --> 00:13:18,280
# The need for the construction of the Ram Temple is to reach all the people in India,

# 156
# 00:13:18,280 --> 00:13:24,280
# To get support from the people and to organize an agitation, they are doing this Ratha Yatra.

# 157
# 00:13:24,280 --> 00:13:29,280
# But as part of this Ratha Yatra, there is a lot of violence in many cities in India.

# 158
# 00:13:29,280 --> 00:13:34,280
# Not only that, an intelligence report that this Babri Mosque could be destroyed immediately,

# 159
# 00:13:34,280 --> 00:13:37,280
# Is also brought to the hands of the government.

# 160
# 00:13:37,280 --> 00:13:40,280
# As part of that, when this Ratha Yatra reached Bihar,

# 161
# 00:13:40,280 --> 00:13:44,280
# According to the order of Lalu Prasad Yadav, who was then the Chief Minister of Bihar,

# 162
# 00:13:44,280 --> 00:13:48,280
# LK Advani is arrested and this Ratha Yatra is suspended.

# 163
# 00:13:48,280 --> 00:13:51,280
# But the Karsevaks, who were part of this Ratha Yatra,

# 164
# 00:13:51,280 --> 00:13:54,280
# That is, the Karsevaks who work as part of these Hindu organizations,

# 165
# 00:13:54,280 --> 00:13:58,280
# The people who are said to be, reach Ayodhya again and organize a large-scale agitation.

# 166
# 00:13:58,280 --> 00:14:03,280
# A large-scale demonstration of about 15,000 Karsevaks is being held in Ayodhya.

# 167
# 00:14:03,280 --> 00:14:06,280
# Against that, according to the order of the then UP government,

# 168
# 00:14:06,280 --> 00:14:11,280
# The police will conduct a raid and kill about 15 Karsevaks.

# 169
# 00:14:11,280 --> 00:14:17,280
# As part of such a big event, the BJP, the then V.P. Singh government, is in power.

# 170
# 00:14:17,280 --> 00:14:20,280
# The V.P. Singh government is also supporting the BJP.

# 171
# 00:14:20,280 --> 00:14:24,280
# The BJP backs up their support and comes to support the government.

# 172
# 00:14:24,280 --> 00:14:28,280
# Within a year, the general election is held in India again.

# 173
# 00:14:28,280 --> 00:14:31,280
# In this general election, the BJP, which had 85 seats last time,

# 174
# 00:14:31,280 --> 00:14:37,280
# Their seat increased by 120 and their vote percentage increased by 9%.

# 175
# 00:14:37,280 --> 00:14:41,280
# In addition, the election to the Lutheran Assembly in 1991 was also held.

# 176
# 00:14:41,280 --> 00:14:44,280
# In the previous election, the BJP had only 57 seats.

# 177
# 00:14:44,280 --> 00:14:47,280
# In the 91st election, the BJP won 221 seats.

# 178
# 00:14:47,280 --> 00:14:52,280
# A government of the BJP leader Kalyan Singh is also in power in Uttar Pradesh.

# 179
# 00:14:52,280 --> 00:14:56,280
# After this, the biggest episode related to Ayodhya takes place.

# 180
# 00:14:56,280 --> 00:15:03,280
# There are reports that there may be attacks on Babri Masjid in Ayodhya and that Babri Masjid may be destroyed.

# 181
# 00:15:03,280 --> 00:15:08,280
# The Supreme Court is asking this question to the Uttar Pradesh government and the central government.

# 182
# 00:15:08,280 --> 00:15:18,280
# The two governments are 100% sure that Babri Masjid will never be destroyed.

# 183
# 00:15:18,280 --> 00:15:20,280
# As the status quo progresses,

# 184
# 00:15:20,280 --> 00:15:31,280
# In 1992, on December 6, some ceremonies were held in the area of Dam Chabutra against the World Hindu Exhibition and other Hindu organizations.

# 185
# 00:15:32,280 --> 00:15:45,280
# For the protection of the disputed area and Babri Masjid, the CRPF and the Uttar Pradesh police were stationed there in large numbers.

# 186
# 00:15:45,280 --> 00:15:55,280
# By surprising everyone, about 1.5 lakh people came to the disputed area of Ayodhya for this operation on December 6.

# 187
# 00:15:55,280 --> 00:16:01,280
# As soon as they arrived, the CRPF officers and the Uttar Pradesh police were outnumbered.

# 188
# 00:16:01,280 --> 00:16:09,280
# At that time, the leaders of this movement, LK Advani, Murali Manohar Joshi, and leaders like Uma Bharathi came here and gave speeches to these people.

# 189
# 00:16:10,280 --> 00:16:25,280
# At around 12 o'clock, about 1.5 lakh CRPF officers and the Uttar Pradesh police began to destroy Babri Masjid using the weapons they had in their hands.

# 190
# 00:16:25,280 --> 00:16:27,280
# It started at 12 o'clock in the afternoon.

# 191
# 00:16:27,280 --> 00:16:32,280
# By 5 o'clock in the evening, the construction of Babri Masjid was in full swing.

# 192
# 00:16:32,280 --> 00:16:41,280
# Not only did they destroy Babri Masjid, but they also built a small temporary temple on top of these ruins.

# 193
# 00:16:41,280 --> 00:16:45,280
# The statue of Ram Lalla, who was inside the mosque earlier, is being erected here.

# 194
# 00:16:45,280 --> 00:16:48,280
# We know that this is a very sensitive issue.

# 195
# 00:16:48,280 --> 00:16:53,280
# Therefore, in the name of this, there will be religious riots and riots in many parts of India.

# 196
# 00:16:53,280 --> 00:16:58,280
# It is estimated that about 2,000 people lost their lives in these riots.

# 197
# 00:16:58,280 --> 00:17:05,280
# This is why the destruction of Babri Masjid is still a black mark in the history of India.

# 198
# 00:17:05,280 --> 00:17:11,280
# So, Kalyan Singh, who promised that there would be no problems with Babri Masjid, had to leave the country at that time.

# 199
# 00:17:11,280 --> 00:17:13,280
# Kalyan Singh's government left the country at that time.

# 200
# 00:17:13,280 --> 00:17:16,280
# Narasimha Rao's government was in power at that time.

# 201
# 00:17:17,280 --> 00:17:22,280
# On December 16, this central government appointed a commission called the Liberhan Commission.

# 202
# 00:17:22,280 --> 00:17:27,280
# This commission was formed to find evidence related to the destruction of Babri Masjid.

# 203
# 00:17:27,280 --> 00:17:29,280
# It was a unique commission.

# 204
# 00:17:29,280 --> 00:17:34,280
# It can be seen that it was the most courageous and most time-consuming commission in the history of India.

# 205
# 00:17:34,280 --> 00:17:37,280
# The duration of this commission is extended at many times.

# 206
# 00:17:37,280 --> 00:17:43,280
# Finally, only in 2009, this commission's report was released to the Parliament.

# 207
# 00:17:43,280 --> 00:17:49,280
# The report states that many of the leaders of the LK administration were guilty of this.

# 208
# 00:17:49,280 --> 00:17:52,280
# The cases related to this are still going on.

# 209
# 00:17:52,280 --> 00:17:55,280
# It should be noted that the final thing has not been done yet.

# 210
# 00:17:55,280 --> 00:18:00,280
# The next major situation is from the side of the PV Narasimha Rao government.

# 211
# 00:18:00,280 --> 00:18:08,280
# The Indian government has acquired 67 acres of land surrounding this disputed land of 2.77 acres.

# 212
# 00:18:08,280 --> 00:18:15,280
# It can be seen that they are acquiring these lands on the basis of a law called the Acquisition of Certain Area at Ayodhya Act of 1993.

# 213
# 00:18:15,280 --> 00:18:21,280
# The Indian government is acquiring this disputed 2.77 acre land as part of this.

# 214
# 00:18:21,280 --> 00:18:27,280
# The next major event is that the Allahabad High Court has brought all these cases under them.

# 215
# 00:18:27,280 --> 00:18:34,280
# In order to settle this case, in 2003, the Allahabad High Court sought the help of the Archaeological Survey of India.

# 216
# 00:18:34,280 --> 00:18:40,280
# In this area, that is, in the disputed area of Ayodhya, various investigations have been going on for a long time.

# 217
# 00:18:40,280 --> 00:18:47,280
# In order to carry out a deeper excavation and investigation, the Allahabad High Court is appealing to the Archaeological Survey of India.

# 218
# 00:18:47,280 --> 00:18:54,280
# As part of this, the Archaeological Survey of India conducted a very in-depth study in this disputed area and submitted its report to the court.

# 219
# 00:18:54,280 --> 00:18:58,280
# Some very important things have been found here by the Archaeological Survey of India.

# 220
# 00:18:58,280 --> 00:19:00,280
# What is that?

# 221
# 00:19:00,280 --> 00:19:04,280
# Many things from history have been found as part of the treasure here.

# 222
# 00:19:04,280 --> 00:19:14,280
# But between the 11th and 12th centuries, they found that there was a large structure under this Babri Mosque.

# 223
# 00:19:14,280 --> 00:19:19,280
# They found that there was a pillar base about 50 meters long to the north-south.

# 224
# 00:19:19,280 --> 00:19:22,280
# There were three structures on top of this pillar base.

# 225
# 00:19:22,280 --> 00:19:24,280
# There was a large structure.

# 226
# 00:19:24,280 --> 00:19:26,280
# They found that there was a large hall in it.

# 227
# 00:19:26,280 --> 00:19:31,280
# Not only that, a very important thing they say is that it was a non-Muslim structure.

# 228
# 00:19:31,280 --> 00:19:34,280
# So this could have been a temple.

# 229
# 00:19:34,280 --> 00:19:39,280
# But the most important thing here is that it was a mosque.

# 230
# 00:19:39,280 --> 00:19:45,280
# Not only that, it is not possible to find that Babri Mosque was built on top of this temple.

# 231
# 00:19:45,280 --> 00:19:50,280
# So there was a large non-Muslim structure there in the 11th and 12th centuries.

# 232
# 00:19:50,280 --> 00:19:53,280
# It is possible to find that there was a mosque in the 16th century.

# 233
# 00:19:53,280 --> 00:19:56,280
# It is not possible for people to find out what happened in between.

# 234
# 00:19:56,280 --> 00:20:02,280
# So based on this evidence and findings, in 2010, the Allahabad High Court passed a law for this case.

# 235
# 00:20:02,280 --> 00:20:04,280
# This is what is said in that law.

# 236
# 00:20:04,280 --> 00:20:07,280
# This disputed area is divided into three.

# 237
# 00:20:07,280 --> 00:20:11,280
# In it, the control of the one-third area is given to Nirmohi Akhara.

# 238
# 00:20:11,280 --> 00:20:14,280
# The control of the one-third area is given to Ram Lalla Virajman.

# 239
# 00:20:14,280 --> 00:20:17,280
# The control of the remaining one-third area is given to Sunni Waqafpur.

# 240
# 00:20:17,280 --> 00:20:23,280
# In this way, the Allahabad High Court is taking a position that this area can be divided into three parties.

# 241
# 00:20:23,280 --> 00:20:26,280
# But many appeals against this are going to the Supreme Court.

# 242
# 00:20:26,280 --> 00:20:30,280
# At the same time, the Supreme Court is staying the law of the Allahabad High Court.

# 243
# 00:20:30,280 --> 00:20:34,280
# Later, we can see that all the cases related to this case are in the Supreme Court.

# 244
# 00:20:34,280 --> 00:20:38,280
# In 2016, J.S.K. Har, who was the Chief Justice of the Supreme Court at that time,

# 245
# 00:20:38,280 --> 00:20:41,280
# He is calling this case a mediation.

# 246
# 00:20:41,280 --> 00:20:45,280
# Because it is a religious issue and a very sensitive issue.

# 247
# 00:20:45,280 --> 00:20:48,280
# Rather than the court taking a decision on this case,

# 248
# 00:20:48,280 --> 00:20:52,280
# It is better that all the parties in it sit together and take a decision.

# 249
# 00:20:52,280 --> 00:20:54,280
# This is a mediation.

# 250
# 00:20:54,280 --> 00:20:57,280
# But there will be no major results as part of that mediation.

# 251
# 00:20:57,280 --> 00:20:59,280
# Not only that, by 2017,

# 252
# 00:20:59,280 --> 00:21:04,280
# Approximately 32 appeals related to this case had reached the Supreme Court.

# 253
# 00:21:04,280 --> 00:21:07,280
# The Supreme Court understands that it is not good for this case to continue like this.

# 254
# 00:21:07,280 --> 00:21:10,280
# As a result, the Supreme Court is taking a decision.

# 255
# 00:21:10,280 --> 00:21:14,280
# In January 2019, the inquiry related to this case will begin.

# 256
# 00:21:14,280 --> 00:21:19,280
# A total of 5 members of the Supreme Court will be on the bench to hear the inquiry of this case.

# 257
# 00:21:19,280 --> 00:21:21,280
# So, all these benches are getting ready.

# 258
# 00:21:21,280 --> 00:21:23,280
# But as a final effort,

# 259
# 00:21:23,280 --> 00:21:25,280
# In March 2019,

# 260
# 00:21:25,280 --> 00:21:28,280
# 3 members of the mediation committee are taking this case again.

# 261
# 00:21:28,280 --> 00:21:31,280
# This is to know whether this case can be resolved through mediation.

# 262
# 00:21:31,280 --> 00:21:35,280
# This mediation committee is submitting their report in May.

# 263
# 00:21:35,280 --> 00:21:37,280
# After that, the case goes to the inquiry.

# 264
# 00:21:37,280 --> 00:21:43,280
# One of the longest inquiries in the history of the Supreme Court is related to the Ayodhya case.

# 265
# 00:21:43,280 --> 00:21:46,280
# This case is being investigated for just a few days.

# 266
# 00:21:46,280 --> 00:21:51,280
# After that, the Supreme Court is reserving the case for November 2019.

# 267
# 00:21:51,280 --> 00:21:54,280
# Thus, on November 9, 2019,

# 268
# 00:21:54,280 --> 00:22:00,280
# The Supreme Court declares the ruling of the Ayodhya case, one of the most important cases in the history of India.

# 269
# 00:22:00,280 --> 00:22:03,280
# So, the Supreme Court had included a lot of things in this ruling.

# 270
# 00:22:03,280 --> 00:22:07,280
# The first thing mentioned in it is that the ruling of the Allahabad High Court is being rejected by the Supreme Court.

# 271
# 00:22:07,280 --> 00:22:11,280
# Because no one related to this case is ready to accept this ruling.

# 272
# 00:22:11,280 --> 00:22:17,280
# If such an arrangement is brought in, it will lead to more problems in the future.

# 273
# 00:22:17,280 --> 00:22:19,280
# So, that ruling is rejected.

# 274
# 00:22:19,280 --> 00:22:23,280
# The most important thing mentioned in this ruling is that Ram Lalla, a party member in this case,

# 275
# 00:22:23,280 --> 00:22:30,280
# has been decided to give the disputed land title of 2.77 acres or its right.

# 276
# 00:22:30,280 --> 00:22:34,280
# So, the Indian government should use the trust associated with this.

# 277
# 00:22:34,280 --> 00:22:41,280
# After using that trust, the Supreme Court has decided to give the disputed land title to them.

# 278
# 00:22:41,280 --> 00:22:47,280
# However, the Supreme Court also says that the Babri Mosque there had been demolished.

# 279
# 00:22:47,280 --> 00:22:51,280
# The destruction of this Babri Mosque is a violation against the rule of law.

# 280
# 00:22:51,280 --> 00:22:54,280
# It was a violation against the rule of law here.

# 281
# 00:22:54,280 --> 00:22:55,280
# It was an illegal activity.

# 282
# 00:22:55,280 --> 00:22:57,280
# So, they should also be given a remedy.

# 283
# 00:22:57,280 --> 00:23:03,280
# As a part of that, the government should be given 5 acres of land in any of the nearby areas,

# 284
# 00:23:03,280 --> 00:23:06,280
# or the 67 acres that the previous government had given,

# 285
# 00:23:06,280 --> 00:23:11,280
# should be given to the Sunni Waqf Board.

# 286
# 00:23:11,280 --> 00:23:15,280
# So, the disputed area is Ram Lalla, a party member in this case.

# 287
# 00:23:15,280 --> 00:23:21,280
# The government says that 5 acres of land should be given to the Sunni Waqf Board, which is the second party.

# 288
# 00:23:21,280 --> 00:23:25,280
# However, we know that there is a third party member in this case, Nirmohi Akhara.

# 289
# 00:23:25,280 --> 00:23:29,280
# However, Nirmohi Akhara's claim, or their right is not in the Supreme Court.

# 290
# 00:23:29,280 --> 00:23:34,280
# The Supreme Court says that they are not able to establish their right here.

# 291
# 00:23:34,280 --> 00:23:36,280
# But the Supreme Court has done one thing.

# 292
# 00:23:36,280 --> 00:23:42,280
# As I said earlier, the disputed land is given to that trust by using the trust of the Central Government.

# 293
# 00:23:42,280 --> 00:23:48,280
# The Supreme Court has decided that Nirmohi Akhara should also have a representative in that trust,

# 294
# 00:23:48,280 --> 00:23:50,280
# and is giving them a relief.

# 295
# 00:23:50,280 --> 00:23:53,280
# These were the three or four important decisions taken by the Supreme Court.

# 296
# 00:23:53,280 --> 00:23:57,280
# However, the Supreme Court has also conducted one or two important investigations.

# 297
# 00:23:57,280 --> 00:23:59,280
# I have already mentioned one of them.

# 298
# 00:23:59,280 --> 00:24:05,280
# In 1992, the Supreme Court found that the demolition of Babri Mosque was an illegal activity,

# 299
# 00:24:05,280 --> 00:24:09,280
# and that it was a violation against the law.

# 300
# 00:24:09,280 --> 00:24:12,280
# Similarly, the second important investigation of the Supreme Court,

# 301
# 00:24:12,280 --> 00:24:20,280
# in 1949, the investigation found that the statues of Hindu gods inside the mosque were also an illegal activity,

# 302
# 00:24:20,280 --> 00:24:22,280
# was also carried out by the Supreme Court as part of this case.

# 303
# 00:24:22,280 --> 00:24:25,280
# So, this was the law put forward by the Supreme Court.

# 304
# 00:24:25,280 --> 00:24:27,280
# Everyone accepted this law.

# 305
# 00:24:27,280 --> 00:24:31,280
# As part of that, the Central Government is using a trust.

# 306
# 00:24:31,280 --> 00:24:34,280
# In the name of Sri Ram Janma Bhoomi Teerth Kshetra Trust,

# 307
# 00:24:34,280 --> 00:24:36,280
# a trust of 15 acres will be used.

# 308
# 00:24:36,280 --> 00:24:43,280
# After using it, as I said earlier, the disputed area of 2.77 acres of land was given to them.

# 309
# 00:24:43,280 --> 00:24:50,280
# Not only that, 67 acres of land acquired by the government in 1993 is also awarded to this trust.

# 310
# 00:24:50,280 --> 00:24:52,280
# This is the government's first decision.

# 311
# 00:24:52,280 --> 00:24:56,280
# As mentioned earlier, 5 acres of land is also awarded to the Sunni Waqf Board.

# 312
# 00:24:56,280 --> 00:25:00,280
# So, the construction of the new Ram Temple is being done on the land that has been awarded like this.

# 313
# 00:25:00,280 --> 00:25:02,280
# This temple is being built on three levels.

# 314
# 00:25:02,280 --> 00:25:04,280
# The construction of the ground floor is now complete.

# 315
# 00:25:04,280 --> 00:25:09,280
# The construction of the other two floors will also be completed by the end of this year.

# 316
# 00:25:09,280 --> 00:25:12,280
# One of the most important inaugurations among them is the Prana Pradishta.

# 317
# 00:25:12,280 --> 00:25:17,280
# That is going to be held by our Prime Minister on the 22nd.

# 318
# 00:25:17,280 --> 00:25:25,280
# So, what is the history of the Ayodhya issue, which has been one of the most important issues in India for 500 years?

# 319
# 00:25:25,280 --> 00:25:27,280
# What are the important developments in it?

# 320
# 00:25:27,280 --> 00:25:30,280
# I hope you have been able to understand from today's video.

# 321
# 00:25:30,280 --> 00:25:33,280
# If you have any comments, suggestions, doubts about this video,

# 322
# 00:25:33,280 --> 00:25:35,280
# or any extra points you know,

# 323
# 00:25:35,280 --> 00:25:37,280
# be sure to write them in the comment box.

# 324
# 00:25:37,280 --> 00:25:40,280
# If you think it's good to see this video to others,

# 325
# 00:25:40,280 --> 00:25:41,280
# you can share this video.

# 326
# 00:25:41,280 --> 00:25:44,280
# Thank you for coming again with such good videos.

# 327
# 00:25:47,280 --> 00:25:48,280
# Thank you.
# """
# #save_as_srt(srt_content, 'youtube.srt')
# print(download_video("https://www.youtube.com/watch?v=GrCWnYsdUNQ&t=368s", srt_content, 'youtube'))
