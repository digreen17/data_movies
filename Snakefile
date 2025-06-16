rule all:
    input:
        "data/processed/processed_data.csv"
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
