import argparse
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from fredapi import Fred

load_dotenv()

SERIES_ID = "CPIAUCNS"
DEFAULT_CPI_PATH = Path("data/raw/cpi_data.csv")


def download_cpi(path: Path) -> None:
    fred = Fred(api_key=os.environ["FRED_KEY"])
    data = fred.get_series(SERIES_ID)

    df_fred = pd.DataFrame(data, columns=["cpi"])
    df_fred.index.name = "year"

    df_fred.to_csv(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download CPI data")
    parser.add_argument(
        "--path",
        type=Path,
        default=DEFAULT_CPI_PATH,
        help="path for saving cpi data",
    )
    args = parser.parse_args()

    download_cpi(args.path)
