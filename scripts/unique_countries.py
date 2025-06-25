import argparse
from pathlib import Path

import pandas as pd

DEFAULT_OUTPUT_PATH = Path("data/processed/processed_data.csv")
COUNTRY_PATH = Path("data/additional/unique_countries.csv")


def unique_countries(input_path: Path, output_path: Path) -> None:
    df = pd.read_csv(input_path, usecols=["production_countries"])
    all_countries = df["production_countries"].str.split(", ").explode().drop_duplicates().sort_values()
    all_countries.to_csv(output_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create unique countries csv")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="path for read csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=COUNTRY_PATH,
        help="path for saving unique_countries csv",
    )
    args = parser.parse_args()

    unique_countries(args.input, args.output)
