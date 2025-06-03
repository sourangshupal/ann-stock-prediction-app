from tensorflow import keras
from logger import setup_logger

model_logger = setup_logger('model', 'logs/model.log')

def build_ann(input_dim):
    model_logger.info('Building ANN model')
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_dim=input_dim),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    model_logger.info('Model built and compiled')
    return model

def train_model(model, X_train, y_train, epochs=50, batch_size=32):
    model_logger.info(f'Training model for {epochs} epochs')
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=0)
    model_logger.info('Model training complete')
    return history

def evaluate_model(model, X_test, y_test):
    model_logger.info('Evaluating model')
    try:
        # model.evaluate returns a list: [loss, metric1, metric2, ...]
        results = model.evaluate(X_test, y_test, verbose=0)
        model_logger.info(f'Evaluation results: {results}')

        if isinstance(results, list) and len(results) >= 2:
            loss, mae = results[0], results[1]
        elif isinstance(results, (int, float)):
            # If only loss is returned
            loss = results
            mae = 0.0
            model_logger.warning('Only loss returned from evaluation, setting MAE to 0')
        else:
            model_logger.error(f'Unexpected evaluation result format: {results}')
            loss, mae = 0.0, 0.0

        model_logger.info(f'Parsed results - Loss: {loss}, MAE: {mae}')
        return loss, mae

    except Exception as e:
        model_logger.error(f'Error during model evaluation: {e}')
        return 0.0, 0.0
