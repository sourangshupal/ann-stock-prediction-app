import argparse
from data_prep import load_and_prepare_data
from model import train_model, evaluate_model, save_model, load_model
from predict import predict
from logger import get_logger

import argparse
import numpy as np
from data_prep import load_data, preprocess_data
from model import build_ann, train_model, evaluate_model
from predict import make_prediction
from logger import setup_logger

def main():
    parser = argparse.ArgumentParser(description='ANN Stock Prediction CLI')
    parser.add_argument('--data', type=str, required=True, help='Path to CSV data file')
    parser.add_argument('--epochs', type=int, default=50, help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size for training')
    parser.add_argument('--predict', type=str, help='Comma-separated feature values for prediction')
    args = parser.parse_args()

    logger = setup_logger('cli', 'logs/cli.log')

    # Data Preparation
    logger.info('Loading and preprocessing data')
    df = load_data(args.data)
    df = preprocess_data(df)
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # Model Training
    logger.info('Building and training model')
    model = build_ann(X_train.shape[1])
    train_model(model, X_train, y_train, epochs=args.epochs, batch_size=args.batch_size)

    # Model Evaluation
    logger.info('Evaluating model')
    loss, mae = evaluate_model(model, X_test, y_test)
    print(f"Evaluation Results - Loss: {loss:.4f}, MAE: {mae:.4f}")

    # Prediction (if requested)
    if args.predict:
        logger.info('Running prediction')
        try:
            X_new = np.array([list(map(float, args.predict.split(',')))])
            pred = make_prediction(model, X_new)
            print(f'Predicted value: {pred[0][0]:.4f}')
        except Exception as e:
            print(f'Prediction error: {e}')

if __name__ == '__main__':
    main()
logger = get_logger("CLI")

def main():
    parser = argparse.ArgumentParser(description="ANN Stock Prediction CLI")
    parser.add_argument('--mode', choices=['train', 'evaluate', 'predict'], required=True, help='Operation mode')
    parser.add_argument('--data', type=str, help='Path to CSV data file')
    parser.add_argument('--model', type=str, default='ann_model.h5', help='Path to save/load model')
    parser.add_argument('--input', type=str, help='Input data for prediction (CSV)')
    args = parser.parse_args()

    if args.mode == 'train':
        logger.info("Starting training mode")
        X_train, X_test, y_train, y_test = load_and_prepare_data(args.data)
        model = train_model(X_train, y_train)
        save_model(model, args.model)
        logger.info("Model trained and saved.")
    elif args.mode == 'evaluate':
        logger.info("Starting evaluation mode")
        X_train, X_test, y_train, y_test = load_and_prepare_data(args.data)
        model = load_model(args.model)
        evaluate_model(model, X_test, y_test)
    elif args.mode == 'predict':
        logger.info("Starting prediction mode")
        model = load_model(args.model)
        X_pred = load_and_prepare_data(args.input, predict_mode=True)
        preds = predict(model, X_pred)
        print("Predictions:", preds)
    else:
        logger.error("Invalid mode selected.")

if __name__ == "__main__":
    main()


# python cli.py --data path/to/your/data.csv --epochs 50 --batch_size 32 --predict "1.2,3.4,5.6,7.8"