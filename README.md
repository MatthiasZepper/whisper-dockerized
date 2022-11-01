# Dockerfiles for OpenAI's Whisper model

This repository contains Dockerfiles to containerize OpenAI's [Whisper ASR model](https://github.com/openai/whisper) and it's dependencies [PyTorch](https://pytorch.org/), [HuggingFace Transformers](https://huggingface.co/docs/transformers/index) and [tokenizers](https://pypi.org/project/tokenizers/). [`ffmpeg`](https://ffmpeg.org/) and [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) are included for media file conversion.

## About the Whisper model

### Architecture and training of the model

Whisper is a general-purpose speech recognition model. It is trained on a large dataset of diverse audio and is also a multi-task model that can perform multilingual speech recognition as well as speech translation and language identification.

It is a transformer sequence-to-sequence model trained on various speech processing tasks, including multilingual speech recognition, speech translation, spoken language identification, and voice activity detection. All of these tasks are jointly represented as a sequence of tokens to be predicted by the decoder, allowing for a single model to replace many different stages of a traditional speech processing pipeline. The multitask training format uses a set of special tokens that serve as task specifiers or classification targets.

Further information is available in the [[blog]](https://openai.com/blog/whisper) and the corresponding [[scientific publication]](https://cdn.openai.com/papers/whisper.pdf)

### Available pre-trained models and languages

There are five model sizes, four with English-only versions, offering speed and accuracy tradeoffs. Below are the names of the available models and their approximate memory requirements and relative speed. 


|  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
|:------:|:----------:|:------------------:|:------------------:|:-------------:|:--------------:|
|  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~32x      |
|  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~16x      |
| small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~6x       |
| medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |

For English-only applications, the `.en` models tend to perform better, especially for the `tiny.en` and `base.en` models. It was observed that the difference becomes less significant for the `small.en` and `medium.en` models.

## Building the containerized versions

To build the containerized version of the Whisper model, local builds are recommended. However, the tiny, base and small models can also still be packaged when run on Github Actions.

By default, the container images contain a cached copy of the `base` model. Set the value of `WHISPER_MODEL` as build argument accordingly to choose a different model. Supported values are listed in the table above. In addition, also the values `all` and `all.en` are legit. Mind that caching too many models will significantly bloat the size of your Docker container image. Provided that there is network access, downloading other models when running the container is still possible.

### Building locally

To build the image locally, Docker (e.g. [Docker Desktop](https://docs.docker.com/desktop)) needs to be installed on your system. Then you can build the image using this Git repository:

```bash
docker build https://github.com/MatthiasZepper/whisper-dockerized.git -t whisper_dockerized:cpu
```

Alternatively, you can also clone this repo beforehand

```bash
git clone https://github.com/MatthiasZepper/whisper-dockerized.git && cd whisper-dockerized
docker build . --file Dockerfile -t whisper_dockerized:cpu
```

To specify the model(s) to be included in the container, set the value of `WHISPER_MODEL` as `--build_arg`:

```bash
docker build https://github.com/MatthiasZepper/whisper-dockerized.git -t whisper_dockerized:cpu --build-arg WHISPER_MODEL=small.en
```

### Running on Github Actions

## Command-line usage

The following command will transcribe speech in audio files, using the `medium` model:

    whisper audio.flac audio.mp3 audio.wav --model medium

The default setting (which selects the `small` model) works well for transcribing English. To transcribe an audio file containing non-English speech, you can specify the language using the `--language` option:

    whisper japanese.wav --language Japanese

Adding `--task translate` will translate the speech into English:

    whisper japanese.wav --language Japanese --task translate

Run the following to view all available options:

    whisper --help

## License

The code and the model weights of Whisper are released under the MIT License and so are the contents of this repository. See [LICENSE](LICENSE) for further details.
