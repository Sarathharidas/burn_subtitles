import os
import yt_dlp
import subprocess
import urllib.parse
from urllib.parse import urlparse


srt_content = """
1
00:00:00,000 --> 00:00:11,800
I recently learned this sweet, quick, little, really effective technique for calming yourself. 

2
00:00:11,800 --> 00:00:15,360
down when you start to feel flustered or anxious.

3
00:00:15,360 --> 00:00:19,240
You've got that sympathetic nervous system kicking in that fight or flight response.

4
00:00:19,240 --> 00:00:25,320
This is a great thing to do and this is so wonderful for both children and adults because

5
00:00:25,320 --> 00:00:32,040
in addition to breathing, deep breathing always helps calm the body, you have a visual and

6
00:00:32,040 --> 00:00:33,800
a tactile component.

7
00:00:33,800 --> 00:00:37,200
So it really pulls your focus and brings you into the moment.

8
00:00:37,200 --> 00:00:39,880
It's called Take 5 Breathing.

9
00:00:39,880 --> 00:00:43,160
And what you'll do is you'll trace your hand.

10
00:00:43,160 --> 00:00:50,160
You put your hand out like this and you're tracing it and as you do that, you'll be breathing

11
00:00:50,160 --> 00:00:59,640
in through the nose, as you go up your finger, out through the mouth, as you go down.

12
00:00:59,640 --> 00:01:07,200
So it's in through the nose, you get to the top, you pause, and you exhale down.

13
00:01:07,200 --> 00:01:08,200
Do it with me.

14
00:01:08,200 --> 00:01:15,760
Let's start at the base of the thumb, breathe in through the nose nice and deep, and out

15
00:01:15,760 --> 00:01:16,760
through the mouth.

16
00:01:16,760 --> 00:01:29,720
Again, in through the nose as you go up, out through the mouth, slide down.

17
00:01:29,720 --> 00:01:44,880
In through the nose, pause, out through the mouth, in, and out.

18
00:01:44,880 --> 00:01:55,600
Last one, in, and out.

19
00:01:55,600 --> 00:01:57,600
How are you feeling?

20
00:01:57,600 --> 00:01:59,200
Did this make a difference for you?

21
00:01:59,200 --> 00:02:01,240
It really does for me.

22
00:02:01,240 --> 00:02:05,720
And you may need to do it more than once, but what a great little trick, right?

23
00:02:05,720 --> 00:02:10,520
If you like it, subscribe and like my video and comment below.

24
00:02:10,520 --> 00:02:12,840
Let me know how this experience went for you.

25
00:02:12,840 --> 00:02:13,600
I'll see you soon.
This is

"""

txt_content = """ I recently learned this sweet, quick, little, really effective technique for calming yourself
down when you start to feel flustered or anxious.
You've got that sympathetic nervous system kicking in that fight or flight response.
This is a great thing to do and this is so wonderful for both children and adults because
in addition to breathing, deep breathing always helps calm the body, you have a visual and
a tactile component.
So it really pulls your focus and brings you into the moment.
It's called Take 5 Breathing.
And what you'll do is you'll trace your hand.
You put your hand out like this and you're tracing it and as you do that, you'll be breathing
in through the nose, as you go up your finger, out through the mouth, as you go down.
So it's in through the nose, you get to the top, you pause, and you exhale down.
Do it with me.
Let's start at the base of the thumb, breathe in through the nose nice and deep, and out
through the mouth.
Again, in through the nose as you go up, out through the mouth, slide down.
In through the nose, pause, out through the mouth, in, and out.
Last one, in, and out.
How are you feeling?
Did this make a difference for you?
It really does for me.
And you may need to do it more than once, but what a great little trick, right?
If you like it, subscribe and like my video and comment below.
Let me know how this experience went for you.
I'll see you soon.
This is """


import requests

# The URL to which the request will be sent


url = 'https://save-subtiles-2-l4365sddta-uc.a.run.app'
# The JSON payload you want to send
payload = {
    'folder_name': '00cf2c45e76c451eb2d1a03f1edd434e',  # Use the S3 link of the video
    'srt_file_content'  : srt_content, ## string format
    'txt_file_content':txt_content  ## ## string format 
    # Add more key-value pairs as needed
}

# Send a POST request
response = requests.post(url, json=payload)
print(response.text)


