import streamlit as st
import pandas as pd
from data_prep import load_data, preprocess_data
from model import build_ann, train_model, evaluate_model
from predict import make_prediction
import numpy as np

st.title('ANN Stock Prediction App')

uploaded_file = st.file_uploader('Upload your stock data CSV', type=['csv'])
if uploaded_file:
    # Load and show initial data
    df = load_data(uploaded_file)
    st.write('**Original Data Preview:**', df.head())
    st.write(f'Original data shape: {df.shape}')
    st.write('Original data types:', df.dtypes)

    # Check if data is empty after loading
    if df.empty:
        st.error("The uploaded file appears to be empty or could not be read properly.")
        st.stop()

    # Preprocess data
    df = preprocess_data(df)

    # Check if data is empty after preprocessing
    if df.empty:
        st.error("All data was removed during preprocessing. Please check your data quality.")
        st.error("Common issues: all values are NaN, non-convertible text data, or empty columns.")
        st.stop()

    st.write('**After Preprocessing:**')
    st.write('Data Preview:', df.head())
    st.write(f'Data shape: {df.shape}')
    st.write('Data types:', df.dtypes)

    # Show what columns will be used for training
    if df.shape[1] >= 2:
        feature_cols = df.columns[:-1].tolist()
        target_col = df.columns[-1]
        st.info(f"**Features (X):** {feature_cols}")
        st.info(f"**Target (y):** {target_col}")
    else:
        st.error("Need at least 2 columns (features + target) for training")
        st.stop()

    # Validate that all columns are numeric
    non_numeric_cols = df.select_dtypes(include=['object']).columns.tolist()
    if non_numeric_cols:
        st.error(f"The following columns contain non-numeric data: {non_numeric_cols}")
        st.error("Please ensure your CSV file contains only numeric data for the model to work properly.")
        st.stop()

    # Check for any remaining NaN or infinite values
    nan_info = df.isnull().sum()
    if nan_info.any():
        st.warning("⚠️ Found missing values after preprocessing:")
        st.write(nan_info[nan_info > 0])

        # Show which rows have NaN values
        rows_with_nan = df.isnull().any(axis=1)
        st.write(f"Rows with missing values: {rows_with_nan.sum()} out of {len(df)}")

        # Option to continue by dropping these rows
        if st.button("🔧 Remove rows with missing values and continue"):
            df_clean = df.dropna()
            if df_clean.empty:
                st.error("No data left after removing missing values!")
                st.stop()
            else:
                df = df_clean
                st.success(f"✅ Removed {len(df) - len(df_clean)} rows. Continuing with {len(df_clean)} rows.")
                st.rerun()
        else:
            st.error("Please click the button above to remove missing values, or fix your data and re-upload.")
            st.stop()

    if np.isinf(df.values).any():
        st.error("Data contains infinite values. Please check your data.")
        st.stop()
    if st.button('Train Model'):
        try:
            # Example: Assume last column is target
            X = df.iloc[:, :-1].values
            y = df.iloc[:, -1].values

            # Ensure data is float32 for TensorFlow compatibility
            X = X.astype(np.float32)
            y = y.astype(np.float32)

            # Validate data shapes and types
            st.write(f'Features shape: {X.shape}, dtype: {X.dtype}')
            st.write(f'Target shape: {y.shape}, dtype: {y.dtype}')

            # Check for minimum data requirements
            if len(X) < 10:
                st.error("Need at least 10 rows of data for training")
                st.stop()

            # Check for any remaining non-finite values
            if not np.isfinite(X).all():
                st.error("Feature data contains non-finite values (NaN or Inf)")
                st.stop()
            if not np.isfinite(y).all():
                st.error("Target data contains non-finite values (NaN or Inf)")
                st.stop()

            split = int(0.8 * len(X))
            if split == 0 or split == len(X):
                st.error("Dataset too small for train/test split. Need at least 5 rows.")
                st.stop()

            X_train, X_test = X[:split], X[split:]
            y_train, y_test = y[:split], y[split:]

            st.write(f'Training set: {X_train.shape[0]} samples')
            st.write(f'Test set: {X_test.shape[0]} samples')

            model = build_ann(X_train.shape[1])
            train_model(model, X_train, y_train)
            loss, mae = evaluate_model(model, X_test, y_test)
            st.success(f'Model trained! Test Loss: {loss:.4f}, MAE: {mae:.4f}')
            st.session_state['model'] = model

        except Exception as e:
            st.error(f'Training error: {str(e)}')
            st.error('Please check your data format and ensure all values are numeric.')
    if 'model' in st.session_state:
        st.subheader('Make Prediction')
        input_data = st.text_input('Enter comma-separated feature values:')
        if st.button('Predict'):
            try:
                X_new = np.array([list(map(float, input_data.split(',')))])
                pred = make_prediction(st.session_state['model'], X_new)
                st.success(f'Predicted value: {pred[0][0]:.4f}')
            except Exception as e:
                st.error(f'Prediction error: {e}')
