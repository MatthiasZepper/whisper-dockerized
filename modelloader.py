import os
import torch
import whisper

# allowed model specifications
allowed_models = {"tiny", "tiny.en", "base.en", "base", "medium", "medium.en", "large"}

# if nothing is specified, default to base
model_name = os.getenv("WHISPER_MODEL", "base")


def cache_model(model_to_load):
    if torch.cuda.is_available():
        whisper.load_model(model_to_load).cuda()
    else:
        whisper.load_model(model_to_load)


if model_name in allowed_models:
    cache_model(model_name)
elif model_name == "all":
    for model in allowed_models:
        cache_model(model)
elif model_name == "all.en":
    for model in list(filter(lambda x: ".en" in x, allowed_models)):
        cache_model(model)
else:
    print("Info: Docker image was built not including any models.")
