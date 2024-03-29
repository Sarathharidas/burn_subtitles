FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

# Install ffmpeg and curl
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app

ENV PORT 8080

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]
