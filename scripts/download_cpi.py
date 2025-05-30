import os
import pandas as pd
from fredapi import Fred 

SERIES_ID = 'CPIAUCNS'

def download_cpi(path):
    fred = Fred(api_key=os.environ['FRED_KEY'])
    data = fred.get_series(SERIES_ID)

    df_fred = pd.DataFrame(data, columns=['cpi'])
    df_fred.index.name = 'year'

    df_fred.to_csv(f'{path}/cpi_data.csv')