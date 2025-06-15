## Скрипты для сбора и обработки данных

- `**download_tmdb.py**` - скрипт для скачивания датасета с Kaggle, с информацией о фильмах. Датасет с Kaggle подгружает данные с сайта TMDB. 

- `**download_cpi.py**` - скрипт для загрузки данных CPI (индекса потребительских цен). Скачивает данные с сайта FRED с помощью API-ключа

- `**process_data.py**` - скрипт для обработки данных. Обрабатывает скачанные данные: фильтрует, объединяет и пересчитывает значения с учётом инфляции.

### Запуск скрипта download_tmdb

`python scripts/download_tmdb.py **--path** path/to/your_file.csv`


- По умолчанию аргумент **--path** сохраняет результат в `data/raw/tmdb_data.csv`

**Важно:** Нужно быть авторизованным в Kaggle CLI, так как в скрипте ссылаемся на KAGGLE_USERNAME и
KAGGLE_KEY

### Запуск скрипта download_cpi

`python scripts/download_cpi.py **--path** path/to/your_file.csv`

- По умолчанию аргумент **--path** сохраняет результат в `data/raw/cpi_data.csv`

**Важно:** Важно получить API-ключ с сайта FRED, так как в скрипте ссылаемся на FRED_KEY



### Запуск скрипта process_data

`python scripts/process_data.py \`
  `**--tmdb** path/to/tmdb.csv \`
  `**--cpi** path/to/cpi.csv \`
  `**--output** path/to/processed.csv`

- `--tmdb` по умолчанию `data/raw/tmdb_data.csv`
- `--cpi` по умолчанию `data/raw/cpi_data.csv`
- `--output` по умолчанию сохраняет обработанные данные в `data/processed/processed_data.csv`


## Запуск тестов

`**make test**` - выполняет юнит-тесты с помощью pytest

## Форматирование кода

`**make format**` - автоматически форматирует python-код с помощью black и сортирует импорты с помощью isort

## Линтинг кода

`**make lint**` - проверяет стиль кода с помощью flake8, black и isort




