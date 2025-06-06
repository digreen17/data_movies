import argparse

import pandas as pd


def process_data(raw_path, save_path):
    df_tmdb = pd.read_csv(
        f"./{raw_path}/tmdb_data.csv",
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
    df_cpi = pd.read_csv(
        f"./{raw_path}/cpi_data.csv",
        parse_dates=["year"],
    ).rename(columns={"year": "cpi_date"})

    latest_cpi = df_cpi.loc[df_cpi["cpi_date"].idxmax(), "cpi"]

    str_column = df_tmdb.select_dtypes(include="object").columns
    for col in str_column:
        df_tmdb[col] = df_tmdb[col].str.lower().str.strip()

    df_tmdb["release_month"] = (
        df_tmdb["release_date"].dt.to_period("M").dt.to_timestamp()
    )

    df_merged = df_tmdb.merge(
        df_cpi, left_on="release_month", right_on="cpi_date", how="left"
    )

    df_merged = df_merged.drop_duplicates(subset=["original_title", "release_date"])

    df_merged = df_merged[df_merged["cpi"].notna()].reset_index(drop=True)

    filter_not_zero = df_merged["revenue"] > 0
    quantile_min = df_merged.loc[filter_not_zero, "revenue"].quantile(0.3)
    quantile_max = df_merged.loc[filter_not_zero, "revenue"].quantile(0.99)

    df_filtered = df_merged[
        (df_merged["revenue"] > quantile_min) & (df_merged["revenue"] < quantile_max)
    ]
    df_filtered = df_filtered.copy()

    df_filtered["main_country"] = df_filtered["production_countries"].str.split(
        ",", expand=True
    )[0]

    df_filtered["genres"] = df_filtered["genres"].fillna("undefined")

    df_filtered["current_budget"] = df_filtered["budget"] * (
        latest_cpi / df_filtered["cpi"]
    )

    df_filtered["current_revenue"] = df_filtered["revenue"] * (
        latest_cpi / df_filtered["cpi"]
    )

    df_filtered = df_filtered[
        [
            "id",
            "title",
            "original_title",
            "original_language",
            "release_date",
            "genres",
            "budget",
            "revenue",
            "vote_average",
            "main_country",
            "cpi",
            "current_budget",
            "current_revenue",
        ]
    ].copy()
    df_filtered = df_filtered.reset_index(drop=True)

    df_filtered.to_csv(f"{save_path}/processed_data.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download CPI and TMDB data")
    parser.add_argument(
        "--raw_path",
        type=str,
        default="data/raw",
        help="path to the directory for saving raw data (default: data/raw)",
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default="data/processed",
        help="path to the directory for saving processed data (default: data/processed)",
    )
    args = parser.parse_args()

    process_data(args.raw_path, args.save_path)
