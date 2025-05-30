from kaggle.api.kaggle_api_extended import KaggleApi

TMDB_DATASET = "asaniczka/tmdb-movies-dataset-2023-930k-movies"


def download_tmdb(path):
    kaggle = KaggleApi()
    kaggle.authenticate()
    kaggle.dataset_download_files(TMDB_DATASET, path=path, unzip=True)
