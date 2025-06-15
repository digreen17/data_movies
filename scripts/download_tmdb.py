import argparse
from pathlib import Path

from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

load_dotenv()

TMDB_DATASET = "asaniczka/tmdb-movies-dataset-2023-930k-movies"
DEFAULT_TMDB_PATH = Path("data/raw/tmdb_data.csv")


def download_tmdb(path: Path) -> None:
    kaggle = KaggleApi()
    kaggle.authenticate()
    kaggle.dataset_download_files(
        TMDB_DATASET, path=path.parent, unzip=True, quiet=False
    )

    csv_files = list(path.parent.glob("TMDB_movie_dataset_*.csv"))
    if not csv_files:
        raise FileNotFoundError("No TMDB .csv file found after unzip")

    original_csv = csv_files[0]
    if original_csv != path:
        original_csv.rename(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download TMDB data")
    parser.add_argument(
        "--path",
        type=Path,
        default=DEFAULT_TMDB_PATH,
        help="path for saving tmdb data",
    )
    args = parser.parse_args()

    download_tmdb(args.path)
