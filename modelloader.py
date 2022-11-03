import os
import torch
import whisper

# allowed model specifications
allowed_models = {
    "tiny",
    "tiny.en",
    "base.en",
    "base",
    "small.en",
    "small",
    "medium",
    "medium.en",
    "large",
}

# if nothing is specified, default to base
model_name = os.getenv("WHISPER_MODEL", "small")
print(f"Downloading {model_name} model(s) to cache inside the container.")


def cache_model(model_to_load):
    print(f"Adding the {model_to_load} model to the container.")
    if torch.cuda.is_available():
        whisper.load_model(model_to_load).cuda()
    else:
        whisper.load_model(model_to_load)


if model_name in allowed_models:
    cache_model(model_name)
elif model_name == "all":
    for model in allowed_models:
        cache_model(model)
    os.environ["WHISPER_MODEL"] = "medium"  # choose a single default model
elif model_name == "all.en":
    for model in list(filter(lambda x: ".en" in x, allowed_models)):
        cache_model(model)
    os.environ["WHISPER_MODEL"] = "medium.en"
else:
    print("Info: Docker image was built not including any models.")
