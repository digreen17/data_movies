import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd

DEFAULT_MIN_Q = 0.3
DEFAULT_MAX_Q = 0.99
DEFAULT_TMDB_PATH = Path("data/raw/tmdb_data.csv")
DEFAULT_CPI_PATH = Path("data/raw/cpi_data.csv")
DEFAULT_OUTPUT_PATH = Path("data/processed/processed_data.csv")


def read_raw_tmdb(path: Path) -> pd.DataFrame:
    return pd.read_csv(
        path,
        usecols=[
            "id",
            "title",
            "original_title",
            "original_language",
            "release_date",
            "genres",
            "budget",
            "revenue",
            "vote_average",
            "production_countries",
        ],
        parse_dates=["release_date"],
    )


def read_raw_cpi(path: Path) -> pd.DataFrame:
    return pd.read_csv(
        path,
        parse_dates=["year"],
    ).rename(columns={"year": "cpi_date"})


def process_tmdb(df_tmdb: pd.DataFrame) -> pd.DataFrame:
    str_column = df_tmdb.select_dtypes(include="object").columns
    for col in str_column:
        df_tmdb[col] = df_tmdb[col].str.lower().str.strip()

    df_tmdb["release_month"] = (
        df_tmdb["release_date"].dt.to_period("M").dt.to_timestamp()
    )
    df_tmdb["main_country"] = df_tmdb["production_countries"].str.split(
        ",", expand=True
    )[0]
    df_tmdb = df_tmdb.drop(columns="production_countries")
    df_tmdb["genres"] = df_tmdb["genres"].fillna("undefined")

    return df_tmdb


def filter_tmdb(
    df_tmdb: pd.DataFrame, min_release_year: datetime, min_q: float, max_q: float
) -> pd.DataFrame:
    required_columns = ["original_title", "release_date", "revenue"]
    missing = set(required_columns) - set(df_tmdb.columns)
    if len(missing) != 0:
        raise ValueError(f"missing required columns: {', '.join(missing)}")
    df_tmdb = df_tmdb.drop_duplicates().reset_index(drop=True)
    df_tmdb = df_tmdb.drop_duplicates(subset=["original_title", "release_date"])
    df_tmdb = df_tmdb.loc[df_tmdb["release_date"] > min_release_year]
    filter_not_zero = df_tmdb["revenue"] > 0
    quantile_min = df_tmdb.loc[filter_not_zero, "revenue"].quantile(min_q)
    quantile_max = df_tmdb.loc[filter_not_zero, "revenue"].quantile(max_q)

    df_filtered = df_tmdb.loc[
        (df_tmdb["revenue"] > quantile_min) & (df_tmdb["revenue"] < quantile_max)
    ]

    return df_filtered


def adjust_inflation(df: pd.DataFrame) -> pd.DataFrame:
    latest_cpi = df.loc[df["cpi_date"].idxmax(), "cpi"]
    df = df.loc[df["cpi"] > 0]
    df["current_budget"] = df["budget"] * (latest_cpi / df["cpi"])
    df["current_revenue"] = df["revenue"] * (latest_cpi / df["cpi"])
    return df


def merge_data(df_tmdb: pd.DataFrame, df_cpi: pd.DataFrame) -> pd.DataFrame:
    df_merged = df_tmdb.merge(
        df_cpi, left_on="release_month", right_on="cpi_date", how="left"
    )
    df_merged = df_merged.drop(columns="release_month")
    df_merged = df_merged[df_merged["cpi"].notna()].reset_index(drop=True)
    return df_merged.reset_index(drop=True)


def process_data(df_tmdb: pd.DataFrame, df_cpi: pd.DataFrame) -> pd.DataFrame:
    df_tmdb = process_tmdb(df_tmdb)
    df_tmdb_filtered = filter_tmdb(
        df_tmdb, df_cpi["cpi_date"].min(), min_q=DEFAULT_MIN_Q, max_q=DEFAULT_MAX_Q
    )
    df_merged = merge_data(df_tmdb_filtered, df_cpi)
    df_final = adjust_inflation(df_merged)
    return df_final


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download CPI and TMDB data")
    parser.add_argument(
        "--tmdb",
        type=Path,
        default=DEFAULT_TMDB_PATH,
        help="path for raw tmdb dataset",
    )
    parser.add_argument(
        "--cpi",
        type=Path,
        default=DEFAULT_CPI_PATH,
        help="path for raw cpi dataset",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="path for saving processed_data",
    )
    args = parser.parse_args()

    df_tmdb = read_raw_tmdb(args.tmdb)
    df_cpi = read_raw_cpi(args.cpi)

    df_filtered = process_data(df_tmdb, df_cpi)

    df_filtered.to_csv(args.output)
