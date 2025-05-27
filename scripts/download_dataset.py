import os
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

load_dotenv()

os.environ['KAGGLE_USERNAME'] = os.getenv('KAGGLE_USERNAME')
os.environ['KAGGLE_KEY'] = os.getenv('KAGGLE_KEY')

api = KaggleApi()
api.authenticate()

# download dataset
dataset = 'asaniczka/tmdb-movies-dataset-2023-930k-movies'
destination = 'data/raw'

os.makedirs(destination, exist_ok=True)

api.dataset_download_files(dataset, path=destination, unzip=True)