import argparse

from dotenv import load_dotenv
from download_cpi import download_cpi
from download_tmdb import download_tmdb


def download_raw(path):
    load_dotenv()

    download_tmdb(path)
    download_cpi(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download CPI and TMDB data")
    parser.add_argument(
        "--path",
        type=str,
        default="data/raw",
        help="path to the directory for saving data (default: data/raw)",
    )
    args = parser.parse_args()

    download_raw(args.path)
