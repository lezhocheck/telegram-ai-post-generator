FROM python:3.11-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt

# install system dependencies
RUN apt-get update && apt-get install -y netcat gcc ffmpeg libsm6 libxext6 \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]