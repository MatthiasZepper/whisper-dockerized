FROM python:3.9.9-slim

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt-get -qq install --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade "pip>=20.3"
RUN pip install poetry

WORKDIR /whisper_asr
COPY . /whisper_asr

RUN poetry config virtualenvs.create false && poetry show
RUN poetry install $(test "${NO_DEV}" && echo "--no-dev") --no-root

# cache the model of choice to allow for offline use.
RUN python3 modelloader.py

ENTRYPOINT ["/usr/local/bin/whisper","--fp16","False"]
CMD ["--help"]