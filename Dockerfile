FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app

ENV PORT 8080

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]