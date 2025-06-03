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
    data_logger.info(f'Starting data preprocessing. Initial shape: {df.shape}')

    # Make a copy to avoid modifying the original
    df = df.copy()

    # Log initial data info
    data_logger.info(f'Initial data types: {df.dtypes.to_dict()}')
    data_logger.info(f'Initial missing values per column: {df.isnull().sum().to_dict()}')

    # Fill missing values using forward fill, then backward fill for any remaining
    df = df.ffill().bfill()
    data_logger.info('Missing values filled with forward and backward fill')

    # Convert all columns to numeric where possible, but skip likely date/text columns
    conversion_results = {}
    date_like_columns = []

    for col in df.columns:
        if df[col].dtype == 'object':
            # Check if this looks like a date column
            if any(keyword in col.lower() for keyword in ['date', 'time', 'timestamp']):
                date_like_columns.append(col)
                data_logger.info(f'Skipping date-like column: {col}')
                continue

            try:
                original_values = df[col].nunique()
                df[col] = pd.to_numeric(df[col], errors='coerce')
                converted_values = df[col].notna().sum()
                conversion_results[col] = f'{converted_values}/{original_values} values converted'
                data_logger.info(f'Converted column {col} to numeric: {conversion_results[col]}')
            except Exception as e:
                data_logger.warning(f'Could not convert column {col} to numeric: {e}')
                conversion_results[col] = f'Failed: {e}'

    # Drop date-like columns since they can't be used for ML
    if date_like_columns:
        df = df.drop(columns=date_like_columns)
        data_logger.info(f'Dropped date-like columns: {date_like_columns}')

    # Log conversion results
    if conversion_results:
        data_logger.info(f'Conversion summary: {conversion_results}')

    # Check how many rows would be lost if we drop NaN
    rows_with_nan = df.isnull().any(axis=1).sum()
    data_logger.info(f'Rows with NaN values: {rows_with_nan} out of {len(df)}')

    # Log which columns have NaN values
    nan_by_column = df.isnull().sum()
    if nan_by_column.any():
        data_logger.info(f'NaN values by column: {nan_by_column[nan_by_column > 0].to_dict()}')

    # Try different strategies to handle NaN values
    if rows_with_nan > 0:
        if rows_with_nan < len(df) * 0.5:  # If less than 50% of rows have NaN
            initial_rows = len(df)
            df = df.dropna()
            final_rows = len(df)
            data_logger.info(f'Dropped {initial_rows - final_rows} rows with NaN values')
        else:
            # Too many rows have NaN, try column-wise approach
            data_logger.warning(f'Too many rows ({rows_with_nan}/{len(df)}) have NaN values')

            # Drop columns that are mostly NaN (>80% NaN)
            nan_threshold = 0.8
            cols_to_drop = []
            for col in df.columns:
                nan_ratio = df[col].isnull().sum() / len(df)
                if nan_ratio > nan_threshold:
                    cols_to_drop.append(col)
                    data_logger.info(f'Column {col} has {nan_ratio:.2%} NaN values - will drop')

            if cols_to_drop:
                df = df.drop(columns=cols_to_drop)
                data_logger.info(f'Dropped columns with >80% NaN: {cols_to_drop}')

            # Now try dropping rows again
            if df.isnull().any().any():
                initial_rows = len(df)
                df = df.dropna()
                final_rows = len(df)
                data_logger.info(f'After column cleanup, dropped {initial_rows - final_rows} rows with NaN values')

    # Final check
    if df.isnull().any().any():
        remaining_nan = df.isnull().sum().sum()
        data_logger.warning(f'Still have {remaining_nan} NaN values after preprocessing')
    else:
        data_logger.info('No NaN values remaining after preprocessing')

    data_logger.info(f'Final preprocessing shape: {df.shape}')
    return df
