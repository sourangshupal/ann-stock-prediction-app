from logger import setup_logger
import numpy as np

predict_logger = setup_logger('predict', 'logs/predict.log')

def make_prediction(model, X):
    predict_logger.info('Making prediction')
    try:
        prediction = model.predict(X)
        predict_logger.info(f'Prediction successful. Output shape: {prediction.shape}')
        return prediction
    except Exception as e:
        predict_logger.error(f'Prediction failed: {e}')
        raise
