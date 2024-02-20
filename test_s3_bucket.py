import os
import yt_dlp
import subprocess
import urllib.parse
from urllib.parse import urlparse


srt_content = """1
00:00:00,000 --> 00:00:05,400
Hi what the fuck?

2
00:00:05,400 --> 00:00:10,200
In this video I'm going to show you how easy it is to deploy a containerized Python flask

3
00:00:10,200 --> 00:00:12,920
application with Amazon LightSail containers.

4
00:00:12,920 --> 00:00:18,520
In this video I'll show you how to create a container service in Amazon LightSail, how

5
00:00:18,520 --> 00:00:24,320
to build a container for a flask application, and how to deploy that container to the container

6
00:00:24,320 --> 00:00:25,320
service.

7
00:00:25,320 --> 00:00:29,280
More information about tutorials to accompany this video is included in the description

8
00:00:29,280 --> 00:00:30,280
below.

9
00:00:30,280 --> 00:00:31,840
Let's get started.

10
00:00:31,840 --> 00:00:37,600
First, log in to your AWS account and navigate to the LightSail web console, and then open

11
00:00:37,600 --> 00:00:40,480
the containers tab.

12
00:00:40,480 --> 00:00:44,480
Here you'll see any existing container services, if you've already created some.

13
00:00:44,480 --> 00:00:48,240
Otherwise, your containers tab will look like this, empty.

14
00:00:48,240 --> 00:00:53,600
Next, create a container service and provide the necessary details for the service, including

15
00:00:53,600 --> 00:00:58,280
the service's location, its capacity, and its name.

16
00:00:58,280 --> 00:01:03,760
The location of your container service indicates which AWS region the service will be in.

17
00:01:03,760 --> 00:01:07,960
You should choose a location for your container service, just like you would if you were launching

18
00:01:07,960 --> 00:01:10,040
a LightSail instance.

19
00:01:10,040 --> 00:01:13,920
Select a region that's close to where the users of the service will be, or you might

20
00:01:13,920 --> 00:01:20,520
have other data sovereignty or regional requirements that will help you make your choice.

21
00:01:20,520 --> 00:01:25,120
The capacity of your container service determines how much power and scale it has.

22
00:01:25,120 --> 00:01:30,280
For a minimal flask app like you're building today, a single micro-node will be okay.

23
00:01:30,280 --> 00:01:34,760
If your capacity requirements change later on, you can easily return and update both

24
00:01:34,760 --> 00:01:38,840
the power and scale of your container service.

25
00:01:38,840 --> 00:01:42,640
The name of your service should follow the naming guidelines and uniqueness constraints

26
00:01:42,640 --> 00:01:43,640
provided.

27
00:01:43,640 --> 00:01:47,600
This name will become part of the default domain name for your container service, so

28
00:01:47,600 --> 00:01:50,520
it needs to be DNS compliant.

29
00:01:50,720 --> 00:01:56,640
Finally, review your container service configuration, make any changes if needed, and then create

30
00:01:56,640 --> 00:01:59,080
the container service.

31
00:01:59,080 --> 00:02:05,040
After a few minutes, your container service will be provisioned and ready for use.

32
00:02:05,040 --> 00:02:10,080
From the container service page, you can create and review deployments, change the service's

33
00:02:10,080 --> 00:02:18,840
capacity, administer custom domains, and view metrics for your service.

34
00:02:18,840 --> 00:02:22,720
Now that you've created your container service, I'll show you how to create and push a Docker

35
00:02:22,720 --> 00:02:26,880
container to your LightSail service from the command line.

36
00:02:26,880 --> 00:02:31,880
Before you get started, you'll need to install Docker, the AWS Command Line Interface, or

37
00:02:31,880 --> 00:02:36,400
CLI, and the LightSail Control Plugin on your system.

38
00:02:36,400 --> 00:02:42,040
Also, I'm using Visual Studio Code and a Linux instance to create and push my container image

39
00:02:42,040 --> 00:02:43,200
to LightSail.

40
00:02:43,200 --> 00:02:49,120
Depending on your system and tools, the UI and commands you use might differ.

41
00:02:49,120 --> 00:02:54,440
To build the container, you'll need three files, the application code, a Python requirements

42
00:02:54,440 --> 00:02:56,560
file, and a Docker file.

43
00:02:56,560 --> 00:03:00,120
Let's look at each one briefly, and then build the container.

44
00:03:00,120 --> 00:03:03,960
The application code defines a minimal Flask application.

45
00:03:03,960 --> 00:03:08,600
It first imports the Flask class and creates an instance of that class.

46
00:03:08,600 --> 00:03:13,600
Next, the route decorator tells Flask what URL should trigger our function, in this

47
00:03:13,600 --> 00:03:15,680
case the root directory.

48
00:03:15,680 --> 00:03:17,920
That's really it.

49
00:03:17,920 --> 00:03:23,320
The requirements text file specifies what Python packages are required by the application.

50
00:03:23,320 --> 00:03:27,920
For this Flask application, there's really only one package required, and that's Flask

51
00:03:27,920 --> 00:03:29,040
itself.

52
00:03:29,040 --> 00:03:33,520
The Docker file specifies how the container image should be built.

53
00:03:33,520 --> 00:03:38,240
The from instruction initializes a new build stage and sets the base image.

54
00:03:38,240 --> 00:03:43,120
We're using an Alpine variant to keep image sizes small.

55
00:03:43,120 --> 00:03:47,520
The expose instruction lets users of this image know that the container will be listening

56
00:03:47,520 --> 00:03:51,680
on port 5000, the default Flask port.

57
00:03:51,680 --> 00:03:56,720
The remainder of the instruction sets the working directory, install dependencies, and

58
00:03:56,720 --> 00:04:00,320
copy the main application code.

59
00:04:00,320 --> 00:04:04,360
Building the container is as simple as running docker build in the same directory as the

60
00:04:04,360 --> 00:04:10,280
Docker file, and providing a tag so we can reference the container later.

61
00:04:10,280 --> 00:04:14,360
You can test your container image locally using the docker run command, and then use

62
00:04:14,360 --> 00:04:19,200
curl or your browser to verify that it's working properly.

63
00:04:19,200 --> 00:04:23,800
After the container is built, push it to the LightSail service you created with the push

64
00:04:23,800 --> 00:04:28,320
container image command provided by the LightSail CLI plugin.

65
00:04:28,320 --> 00:04:32,400
This command includes the name of the container services you created in the previous section

66
00:04:32,440 --> 00:04:35,840
as well as the tag for the container image you just built.

67
00:04:35,840 --> 00:04:39,640
This command stores the container image with your container service.

68
00:04:39,640 --> 00:04:45,640
Now you can reference it by its unique ID when you create a deployment.

69
00:04:45,640 --> 00:04:49,240
Now that the service has been created and the container image built, we'll return to

70
00:04:49,240 --> 00:04:53,360
the LightSail console to deploy your container service.

71
00:04:53,360 --> 00:04:58,600
Back on the container service page, you'll see a new tab has appeared called images.

72
00:04:58,600 --> 00:05:02,280
This is where you can view and administer the images stored with your LightSail container

73
00:05:02,280 --> 00:05:04,160
service.

74
00:05:04,160 --> 00:05:11,120
On the deployments tab, create a new service and provide the necessary parameters.

75
00:05:11,120 --> 00:05:15,720
Provide a unique name for this container and specify the image the container should use.

76
00:05:15,720 --> 00:05:19,680
In this case, the image you created in the previous section, but you could also provide

77
00:05:19,680 --> 00:05:23,280
the name of a container in a public repository.

78
00:05:23,280 --> 00:05:29,280
Next, specify the configuration for the container, including the run command, and any environmental

79
00:05:29,280 --> 00:05:31,800
variables or open ports.

80
00:05:31,800 --> 00:05:38,800
Our flask application uses the flask run command and also needs to know where the flask app

81
00:05:38,800 --> 00:05:40,800
is located.

82
00:05:40,800 --> 00:05:48,800
In addition, we'll specify which port the flask app is listening on, port 5000.

83
00:05:48,800 --> 00:05:51,800
Finally, create a public endpoint.

84
00:05:51,800 --> 00:05:57,800
A public endpoint allows end users or consumers of your service to reach it from the Internet.

85
00:05:57,800 --> 00:06:02,800
LightSail will create a secure public HTTPS endpoint for your service that is accessible

86
00:06:02,800 --> 00:06:07,800
through the default domain name.

87
00:06:07,800 --> 00:06:11,800
Once your service has been deployed, you can visit the public endpoint with your browser

88
00:06:11,800 --> 00:06:14,800
by clicking on the link on the service page.

89
00:06:14,800 --> 00:06:18,800
Here you can verify that your flask application has been deployed correctly and is accepting

90
00:06:18,800 --> 00:06:22,800
traffic from the Internet.

91
00:06:22,800 --> 00:06:26,800
Once you've verified that your container service is operating correctly and you're finished

92
00:06:26,800 --> 00:06:31,800
with it, you can easily delete your LightSail container service and all resources associated

93
00:06:31,800 --> 00:06:41,800
with it, including deployments and saved container images.

94
00:06:41,800 --> 00:06:45,800
In this video, I've shown you how easy it is to deploy a flask application in the cloud

95
00:06:45,800 --> 00:06:47,800
using LightSail containers.

96
00:06:47,800 --> 00:06:52,800
I demonstrated how to create a container service using the LightSail web console, how to create

97
00:06:52,800 --> 00:06:56,800
and push a Docker container to your LightSail service from the command line, and then how

98
00:06:56,800 --> 00:07:01,800
to deploy your container from the console.

99
00:07:01,800 --> 00:07:05,800
Amazon LightSail containers is an easy way to get started with containers in the cloud,

100
00:07:05,800 --> 00:07:11,800
particularly for startups, developers, and hobbyists taking their first steps into containerization.

101
00:07:11,800 --> 00:07:15,800
You can use the Amazon LightSail containers to learn more about containers in the cloud,

102
00:07:15,800 --> 00:07:20,800
to gain experience running containers in the cloud, and along the way benefit from simple

103
00:07:20,800 --> 00:07:23,800
container orchestration.

104
00:07:23,800 --> 00:07:27,800
For more information about Amazon LightSail containers, please visit the LightSail product

105
00:07:27,800 --> 00:07:28,800
page.4444444

106
00:07:28,800 --> 00:07:29,800
Thank you.


"""



import requests

# The URL to which the request will be sent
url = 'https://burn-subtitle-2-l4365sddta-uc.a.run.app'

#url = 'http://127.0.0.1:8080'
# The JSON payload you want to send
payload = {
    'video_link': 'https://quick-translates.s3.amazonaws.com/user_uploads/13babe8d90ed4451afb42453adfa013f.mp4',  # Use the S3 link of the video
    'srt_file_content'  : srt_content,
    's3_youtube_flag':'s3'  ## Fla
    
    # Add more key-value pairs as needed
}

# Send a POST request
response = requests.post(url, json=payload)
print(response.text)


