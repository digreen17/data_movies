from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

TMDB_DATASET = "asaniczka/tmdb-movies-dataset-2023-930k-movies"
DATA_RAW_PATH = "data/raw"


def download_dataset():
    load_dotenv()

    api = KaggleApi()
    api.authenticate()

    api.dataset_download_files(TMDB_DATASET, path=DATA_RAW_PATH, unzip=True)


if __name__ == "__main__":
    download_dataset()
