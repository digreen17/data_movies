import argparse
from pathlib import Path

import pandas as pd

DEFAULT_OUTPUT_PATH = Path("data/processed/processed_data.csv")
GENRES_PATH = Path("data/processed/unique_genres.csv")


def unique_genres(input_path: Path, output_path: Path) -> None:
    df = pd.read_csv(input_path, usecols=["genres"])
    all_genres = df["genres"].str.split(", ").explode().drop_duplicates().sort_values()
    all_genres.to_csv(output_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create unique genres csv")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="path for read csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=GENRES_PATH,
        help="path for saving unique_genres csv",
    )
    args = parser.parse_args()

    unique_genres(args.input, args.output)
