import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from scripts.process_data import adjust_inflation, filter_tmdb, merge_data, process_tmdb

# 1) Проверка наличия столбцов: ["original_title", "release_date", "revenue"]
# 2) Проверить что столбец "revenue" является numeric
# 3) Проверить release_date является datetime
# 4) Проверить, что значения min_q, max_q [0...1]
# 5) Проверить что будет, если все revenue = 0
# 6) Проверить, что  будет, если min_q = max_q


@pytest.mark.parametrize(
    "df_input, df_want, min_release_year, min_q, max_q",
    [
        # Проверка корректности работы фильтрации по квантилям
        (
            pd.DataFrame(
                {
                    "original_title": ["the holiday", "hilch", "spy"],
                    "release_date": pd.to_datetime(
                        ["2022-08-01", "2021-07-01", "2021-06-01"]
                    ),
                    "revenue": [400.0, 300.0, 200.0],
                }
            ),
            pd.DataFrame(
                {
                    "original_title": ["hilch"],
                    "release_date": pd.to_datetime(["2021-07-01"]),
                    "revenue": [300.0],
                }
            ),
            pd.to_datetime("2018-08-01"),
            0,
            1,
        ),
        # Проверка корректности работы фильтрации по минимальной дате
        (
            pd.DataFrame(
                {
                    "original_title": ["the holiday", "hilch", "spy"],
                    "release_date": pd.to_datetime(
                        ["2018-08-01", "2018-07-01", "2018-06-01"]
                    ),
                    "revenue": [400.0, 300.0, 200.0],
                }
            ),
            pd.DataFrame(
                {
                    "original_title": pd.Series([], dtype="object"),
                    "release_date": pd.to_datetime([]),
                    "revenue": pd.Series([], dtype="float64"),
                }
            ),
            pd.to_datetime("2018-08-01"),
            0,
            0.99,
        ),
        # Проверка корректности работы фильтрации по revenue > 0
        (
            pd.DataFrame(
                {
                    "original_title": ["the holiday", "hilch", "spy"],
                    "release_date": pd.to_datetime(
                        ["2021-08-01", "2021-07-01", "2021-06-01"]
                    ),
                    "revenue": [0.0, 0.0, 0.0],
                }
            ),
            pd.DataFrame(
                {
                    "original_title": pd.Series([], dtype="object"),
                    "release_date": pd.to_datetime([]),
                    "revenue": pd.Series([], dtype="float64"),
                }
            ),
            pd.to_datetime("2018-08-01"),
            0,
            1,
        ),
        # Проверка фильтрации по квантилям при двух значениях
        (
            pd.DataFrame(
                {
                    "original_title": ["movie_1", "the holiday"],
                    "release_date": pd.to_datetime(["2021-06-01", "2021-07-01"]),
                    "revenue": [200.0, 300.0],
                }
            ),
            pd.DataFrame(
                {
                    "original_title": pd.Series([], dtype="object"),
                    "release_date": pd.to_datetime([]),
                    "revenue": pd.Series([], dtype="float64"),
                }
            ),
            pd.to_datetime("2018-08-01"),
            0,
            1,
        ),
    ],
)
def test_filter_happy_path(df_input, df_want, min_release_year, min_q, max_q):

    df_result = filter_tmdb(df_input, min_release_year, min_q, max_q)
    df_result = df_result.reset_index(drop=True)
    assert_frame_equal(df_result, df_want)


# Тест, проверяющий наличие ошибки при отсутсвии столбца с названием original_title
def test_absence_columns():
    df = pd.DataFrame(
        {
            "not_current_title": pd.Series([], dtype="object"),
            "release_date": pd.to_datetime([]),
            "revenue": pd.Series([], dtype="float64"),
            "additional_column": pd.Series([]),
        }
    )
    with pytest.raises(ValueError, match="missing required columns: original_title"):
        filter_tmdb(df, min_release_year=pd.to_datetime("2018-08-01"), min_q=0, max_q=1)


# Тест, проверяющий наличие ошибки при значении квантиля больше 1
# (допустимый интервал для функции quentile() = [0, 1])
def test_invalid_quantile():
    df = pd.DataFrame(
        {
            "original_title": ["movie_1", "the holiday", "hilch", "spy"],
            "release_date": pd.to_datetime(
                ["2021-06-01", "2021-07-01", "2021-08-01", "2021-09-01"]
            ),
            "revenue": [200.0, 300.0, 400.0, 500.0],
        }
    )
    with pytest.raises(
        ValueError, match=r"percentiles should all be in the interval \[0, 1\]"
    ):
        filter_tmdb(
            df, min_release_year=pd.to_datetime("2018-08-01"), min_q=0, max_q=10
        )


@pytest.mark.parametrize(
    "df_input, df_want",
    [
        # Проверка преобразования строковых значений к нижнему регистру
        # и удаления пробелов в начале и конце строки
        (
            pd.DataFrame(
                {
                    "genres": [" drAMa, RomaNce "],
                    "release_date": pd.to_datetime(["2021-08-20"]),
                    "production_countries": [" FrANce"],
                }
            ),
            pd.DataFrame(
                {
                    "genres": ["drama, romance"],
                    "release_date": pd.to_datetime(["2021-08-20"]),
                    "release_month": pd.to_datetime(["2021-08-01"]),
                    "main_country": ["france"],
                }
            ),
        ),
        # Проверка вывода main_country - production_countries разделяется по ","
        # и выводится 0 индекс, то есть первая страна в списке
        (
            pd.DataFrame(
                {
                    "genres": ["genre_1"],
                    "release_date": pd.to_datetime(["2021-08-20"]),
                    "production_countries": ["spain, france, japan"],
                }
            ),
            pd.DataFrame(
                {
                    "genres": ["genre_1"],
                    "release_date": pd.to_datetime(["2021-08-20"]),
                    "release_month": pd.to_datetime(["2021-08-01"]),
                    "main_country": ["spain"],
                }
            ),
        ),
        # Проверка того, что значения release_month выводятся в виде - ГГГГ-ММ-01
        (
            pd.DataFrame(
                {
                    "genres": ["genre_1", "genre_2", "genre_3"],
                    "release_date": pd.to_datetime(
                        ["2021-08-20", "2021-07-01", "2021-06-11"]
                    ),
                    "production_countries": ["country_1", "country_2", "country_2"],
                }
            ),
            pd.DataFrame(
                {
                    "genres": ["genre_1", "genre_2", "genre_3"],
                    "release_date": pd.to_datetime(
                        ["2021-08-20", "2021-07-01", "2021-06-11"]
                    ),
                    "release_month": pd.to_datetime(
                        ["2021-08-01", "2021-07-01", "2021-06-01"]
                    ),
                    "main_country": ["country_1", "country_2", "country_2"],
                }
            ),
        ),
        (
            pd.DataFrame(
                {
                    "genres": [None, None, "genre_3"],
                    "release_date": pd.to_datetime(
                        ["2021-08-20", "2021-07-01", "2021-06-11"]
                    ),
                    "production_countries": ["country_1", "country_2", "country_2"],
                }
            ),
            pd.DataFrame(
                {
                    "genres": ["undefined", "undefined", "genre_3"],
                    "release_date": pd.to_datetime(
                        ["2021-08-20", "2021-07-01", "2021-06-11"]
                    ),
                    "release_month": pd.to_datetime(
                        ["2021-08-01", "2021-07-01", "2021-06-01"]
                    ),
                    "main_country": ["country_1", "country_2", "country_2"],
                }
            ),
        ),
    ],
)
def test_process_tmdb_happy_path(df_input, df_want):
    df_output = process_tmdb(df_input)
    df_output = df_output.reset_index(drop=True)
    assert_frame_equal(df_output, df_want)


@pytest.mark.parametrize(
    "df_tmdb, df_cpi, df_want",
    [
        # Проверка, что при совпадении по столбцам "release_month"
        # и "cpi_date" мержатся данные
        (
            pd.DataFrame({"release_month": pd.to_datetime(["2021-08-01"])}),
            pd.DataFrame({"cpi_date": pd.to_datetime(["2021-08-01"]), "cpi": [202]}),
            pd.DataFrame({"cpi_date": pd.to_datetime(["2021-08-01"]), "cpi": [202]}),
        ),
        # Проверка, что, при несовпадении по "release_month" и "cpi_date",
        # по столбцам "cpi_date" и "cpi" будут пустые значения
        (
            pd.DataFrame({"release_month": pd.to_datetime(["2021-08-01"])}),
            pd.DataFrame({"cpi_date": pd.to_datetime(["2021-07-01"]), "cpi": [202]}),
            pd.DataFrame(
                {
                    "cpi_date": pd.to_datetime([]),
                    "cpi": [],
                }
            ),
        ),
    ],
)
def test_merge_data_happy_path(df_tmdb, df_cpi, df_want):
    df_output = merge_data(df_tmdb, df_cpi)
    df_output = df_output.reset_index(drop=True)
    assert_frame_equal(df_output, df_want)


#  Тест, который проверяет наличие ошибки при отсутствии столбца "release_month"
#  по которому мы мержим данные с "cpi_date"
def test_absence_merge_columns():
    df_tmdb = pd.DataFrame(
        {
            "not_current_title": pd.Series([], dtype="object"),
        }
    )
    df_cpi = pd.DataFrame(
        {
            "cpi_date": pd.to_datetime([]),
            "cpi": pd.Series([], dtype="float64"),
        }
    )
    with pytest.raises(KeyError, match="release_month"):
        merge_data(df_tmdb, df_cpi)


@pytest.mark.parametrize(
    "df_input, df_want",
    [
        # Проверка рассчета с учетом инфляции для нормальных значений CPI
        (
            pd.DataFrame(
                {
                    "cpi_date": pd.to_datetime(["2021-08-01", "2021-12-01"]),
                    "cpi": [100.0, 200.0],
                    "budget": [1000.0, 2000.0],
                    "revenue": [1000.0, 2000.0],
                }
            ),
            pd.DataFrame(
                {
                    "cpi_date": pd.to_datetime(["2021-08-01", "2021-12-01"]),
                    "cpi": [100.0, 200.0],
                    "budget": [1000.0, 2000.0],
                    "revenue": [1000.0, 2000.0],
                    "current_budget": [
                        (1000.0 * 200.0 / 100.0),
                        (2000.0 * 200.0 / 200.0),
                    ],
                    "current_revenue": [
                        (1000.0 * 200.0 / 100.0),
                        (2000.0 * 200.0 / 200.0),
                    ],
                }
            ),
        ),
    ],
)
def test_adjust_inflation_happy_path(df_input, df_want):
    df_output = adjust_inflation(df_input)
    df_output = df_output.reset_index(drop=True)
    assert_frame_equal(df_output, df_want)


# Тест, который проверяет наличие ошибки при невозможности
# найти индекс максимального значения в пустом массиве
def test_adjust_empty_cpi_date():
    df = pd.DataFrame(
        {
            "cpi_date": pd.to_datetime([]),
            "cpi": pd.Series([], dtype="float64"),
            "budget": pd.Series([], dtype="float64"),
            "revenue": pd.Series([], dtype="float64"),
        }
    )
    with pytest.raises(ValueError, match="attempt to get argmax of an empty sequence"):
        adjust_inflation(df)
