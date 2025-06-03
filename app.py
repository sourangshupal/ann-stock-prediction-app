import streamlit as st
import pandas as pd
from data_prep import load_data, preprocess_data
from model import build_ann, train_model, evaluate_model
from predict import make_prediction
import numpy as np

st.title('ANN Stock Prediction App')

uploaded_file = st.file_uploader('Upload your stock data CSV', type=['csv'])
if uploaded_file:
    df = load_data(uploaded_file)
    df = preprocess_data(df)
    st.write('Data Preview:', df.head())
    if st.button('Train Model'):
        # Example: Assume last column is target
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values
        split = int(0.8 * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        model = build_ann(X_train.shape[1])
        train_model(model, X_train, y_train)
        loss, mae = evaluate_model(model, X_test, y_test)
        st.success(f'Model trained! Test Loss: {loss:.4f}, MAE: {mae:.4f}')
        st.session_state['model'] = model
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
