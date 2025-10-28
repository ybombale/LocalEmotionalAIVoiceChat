"""
Python script to download the models from Huggingface's model hub.
Originally copied from https://github.com/KoljaB/Linguflex/blob/main/download_models.py
Modified by me to download needed models here - BUT not tested yet

NOTE: Maybe will be needed to 'pip install huggingface_hub' before using it.
"""

from huggingface_hub import hf_hub_download
import os


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def create_directories():
    create_directory("models")
    create_directory("models/xtts")
    create_directory("models/xtts/Lasinya")
    #create_directory("models/llm")

def download_file(
        url,
        filename_server,
        path_local
        ):

    local_file = os.path.join(path_local, filename_server)
    if os.path.exists(local_file):
        print(f"File {filename_server} already exists in {path_local}.")
        return

    print(f"Downloading {filename_server} from repo {url} to {path_local}")
    hf_hub_download(
        repo_id=url,
        filename=filename_server,
        local_dir=path_local)


create_directories()

# download xtts trained model files
print("Downloading xtts trained model files (Lasinya)")
download_file(
     "KoljaB/XTTS_Lasinya", "config.json", "models/xtts/Lasinya")
download_file(
     "KoljaB/XTTS_Lasinya", "vocab.json", "models/xtts/Lasinya")
download_file(
     "KoljaB/XTTS_Lasinya", "speakers_xtts.pth", "models/xtts/Lasinya")
download_file(
     "KoljaB/XTTS_Lasinya", "model.pth", "models/xtts/Lasinya")


# download default local llm file
# print("Downloading default local llm model file")
# download_file(
#     "TheBloke/OpenHermes-2.5-Mistral-7B-GGUF",
#     "openhermes-2.5-mistral-7b.Q5_K_M.gguf", "models/llm")
