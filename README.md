# Data Movies

ETL-пайплайн для сбора и подготовки данных к дашборду **DataLense**.

[Перейти к дашборду](placeholder)

## Источники данных

### TMDB Movie Dataset
Полный датасет фильмов с платформы Kaggle:  
[Ссылка на источник](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies)  
Обновляется ежедневно.

### FRED (Federal Reserve Bank of St. Louis)
Источник данных по инфляции (индекс потребительских цен — CPI):  
[Ссылка на источник](https://fred.stlouisfed.org/series/CPIAUCNS)  
Обновление ежемесячно.

## Установка

1. Создайте файл `.env` на основе шаблона `.env.example`:
   - Укажите переменные `KAGGLE_USERNAME`, `KAGGLE_KEY`
   - Добавьте API-ключ `FRED_KEY`

2. Установите зависимости:
```bash
make install
```

## ETL

![DAG](./references/dag.png)

Для скачивания и обработки данных:
```bash
make etl
```

## Тестирование и проверка кода
```bash
make test    # запускает юнит-тесты (pytest)
make format  # автоформатирование black + isort
make lint    # проверка flake8, black, isort
```

## Лицензия
Проект распространяется под лицензией [MIT](LICENSE).

