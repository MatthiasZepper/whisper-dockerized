FROM python:3.9.9-slim

ARG WHISPER_MODEL
ENV WHISPER_MODEL=$WHISPER_MODEL
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -qq update && \
    apt-get -qq install --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir "poetry>=1.2.0"

WORKDIR "/whisper_asr"
COPY . "/whisper_asr"

RUN poetry config virtualenvs.create false && poetry lock --no-update
RUN poetry install --only main --no-root

# cache the model of choice to allow for offline use.
RUN python3 modelloader.py

CMD [ "/bin/bash", "-l","-c"]