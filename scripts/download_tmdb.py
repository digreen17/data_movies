import os

from kaggle.api.kaggle_api_extended import KaggleApi

TMDB_DATASET = "asaniczka/tmdb-movies-dataset-2023-930k-movies"


def download_tmdb(path: str) -> None:
    kaggle = KaggleApi()
    kaggle.authenticate()
    kaggle.dataset_download_files(TMDB_DATASET, path=path, unzip=True)

    os.rename(f"{path}/TMDB_movie_dataset_v11.csv", f"{path}/tmdb_data.csv")
