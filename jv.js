// Assuming you're using this in a Node.js environment, you might need to install node-fetch
// npm install node-fetch
// If you're running this in a browser, 'fetch' is available by default and you don't need to import it.

const fetch = require('node-fetch'); // Remove this line if you're using this in a browser environment

const srtContent = `1
00:00:00,000 --> 00:00:05,400
Hi what the fuck?

2
00:00:05,400 --> 00:00:10,200
In this video I'm going to show you how easy it is to deploy a containerized Python flask

...

105
00:07:27,800 --> 00:07:28,800
page.4444444

106
00:07:28,800 --> 00:07:29,800
Thank you.
`;

const url = 'https://burn-subtitle-2-l4365sddta-uc.a.run.app';

const payload = {
    video_link: 'https://quick-translates.s3.amazonaws.com/user_uploads/13babe8d90ed4451afb42453adfa013f.mp4',
    srt_file_content: srtContent,
    s3_youtube_flag: 's3'
};

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
})
.then(response => response.text())
.then(text => console.log(text))
.catch(error => console.error('Error:', error));
