import pandas as pd
from logger import setup_logger

data_logger = setup_logger('data_prep', 'logs/data_prep.log')

def load_data(filepath):
    data_logger.info(f'Loading data from {filepath}')
    try:
        df = pd.read_csv(filepath)
        data_logger.info(f'Data loaded successfully. Shape: {df.shape}')
        return df
    except Exception as e:
        data_logger.error(f'Error loading data: {e}')
        raise

def preprocess_data(df):
    data_logger.info('Starting data preprocessing')
    # Example: fill missing values
    df = df.fillna(method='ffill')
    data_logger.info('Missing values filled')
    # Add more preprocessing as needed
    return df
