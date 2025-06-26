rule all:
    input:
        "data/additional/unique_genres.csv",
        "data/additional/unique_countries.csv"
rule download_cpi:
    output:
        "data/raw/cpi_data.csv"
    shell:
        "python scripts/download_cpi.py --path {output}"
rule download_tmdb:
    output:
        "data/raw/tmdb_data.csv"
    shell:
        "python scripts/download_tmdb.py --path {output}"
rule process_data:
    input:
        tmdb="data/raw/tmdb_data.csv",
        cpi="data/raw/cpi_data.csv"
    output:
        "data/processed/processed_data.csv"
    shell:
        """python scripts/process_data.py --tmdb {input.tmdb} --cpi {input.cpi} --output {output}"""
rule unique_genres:
    input:
        "data/processed/processed_data.csv"
    output:
        "data/additional/unique_genres.csv"
    shell:
        """python scripts/unique_genres.py --input {input} --output {output}"""
rule unique_countries:
    input:
        "data/processed/processed_data.csv"
    output:
        "data/additional/unique_countries.csv"
    shell:
        """python scripts/unique_countries.py --input {input} --output {output}"""