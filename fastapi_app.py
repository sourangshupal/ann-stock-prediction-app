#!/usr/bin/env python3
"""
FastAPI Web Server for ANN Stock Prediction App
Provides REST API endpoints for training, prediction, and evaluation
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
import io
import json
import os
from datetime import datetime
import tempfile
import traceback

# Import our existing modules
from data_prep import load_data, preprocess_data
from model import build_ann, train_model, evaluate_model
from predict import make_prediction
from logger import setup_logger

# Setup logger
api_logger = setup_logger('fastapi', 'logs/fastapi.log')

# Initialize FastAPI app
app = FastAPI(
    title="ANN Stock Prediction API",
    description="REST API for training, evaluating, and making predictions with ANN stock prediction model",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Global model storage
current_model = None
model_metadata = {}

# Pydantic models for request/response
class TrainingResponse(BaseModel):
    status: str
    message: str
    model_id: str
    training_time: float
    data_shape: List[int]
    train_samples: int
    test_samples: int
    loss: Optional[float] = None
    mae: Optional[float] = None

class PredictionRequest(BaseModel):
    features: List[float] = Field(..., description="Feature values for prediction")
    
class PredictionResponse(BaseModel):
    status: str
    prediction: float
    model_id: str
    timestamp: str

class EvaluationResponse(BaseModel):
    status: str
    model_id: str
    loss: float
    mae: float
    test_samples: int
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_id: Optional[str] = None
    timestamp: str

@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "ANN Stock Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "train": "/train",
            "predict": "/predict", 
            "evaluate": "/evaluate",
            "health": "/health",
            "docs": "/docs"
        },
        "model_loaded": current_model is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        model_loaded=current_model is not None,
        model_id=model_metadata.get("model_id"),
        timestamp=datetime.now().isoformat()
    )

@app.post("/train", response_model=TrainingResponse)
async def train_model_endpoint(
    file: UploadFile = File(..., description="CSV file with training data"),
    epochs: int = Query(50, ge=1, le=1000, description="Number of training epochs"),
    batch_size: int = Query(32, ge=1, le=512, description="Batch size for training"),
    test_split: float = Query(0.2, ge=0.1, le=0.5, description="Fraction of data for testing")
):
    """
    Train a new ANN model with uploaded data
    
    - **file**: CSV file containing stock data
    - **epochs**: Number of training epochs (1-1000)
    - **batch_size**: Batch size for training (1-512)
    - **test_split**: Fraction of data for testing (0.1-0.5)
    """
    global current_model, model_metadata
    
    try:
        api_logger.info(f"Starting model training with epochs={epochs}, batch_size={batch_size}")
        start_time = datetime.now()
        
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV file")
        
        # Read uploaded file
        contents = await file.read()
        csv_data = io.StringIO(contents.decode('utf-8'))
        
        # Load and preprocess data
        api_logger.info("Loading and preprocessing data")
        df = pd.read_csv(csv_data)
        df = preprocess_data(df)
        
        if df.empty:
            raise HTTPException(status_code=400, detail="No valid data after preprocessing")
        
        if df.shape[1] < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 columns (features + target)")
        
        # Prepare training data
        X = df.iloc[:, :-1].values.astype(np.float32)
        y = df.iloc[:, -1].values.astype(np.float32)
        
        # Split data
        split_idx = int((1 - test_split) * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        if len(X_train) < 5 or len(X_test) < 2:
            raise HTTPException(status_code=400, detail="Insufficient data for training and testing")
        
        # Build and train model
        api_logger.info(f"Building model with input dimension: {X_train.shape[1]}")
        model = build_ann(X_train.shape[1])
        
        api_logger.info("Training model")
        train_model(model, X_train, y_train, epochs=epochs, batch_size=batch_size)
        
        # Evaluate model
        api_logger.info("Evaluating model")
        loss, mae = evaluate_model(model, X_test, y_test)
        
        # Store model and metadata
        model_id = f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        current_model = model
        model_metadata = {
            "model_id": model_id,
            "created_at": datetime.now().isoformat(),
            "input_features": X_train.shape[1],
            "training_samples": len(X_train),
            "test_samples": len(X_test),
            "epochs": epochs,
            "batch_size": batch_size,
            "loss": loss,
            "mae": mae
        }
        
        training_time = (datetime.now() - start_time).total_seconds()
        api_logger.info(f"Model training completed in {training_time:.2f} seconds")
        
        return TrainingResponse(
            status="success",
            message="Model trained successfully",
            model_id=model_id,
            training_time=training_time,
            data_shape=list(df.shape),
            train_samples=len(X_train),
            test_samples=len(X_test),
            loss=loss,
            mae=mae
        )
        
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"Training failed: {str(e)}")
        api_logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(request: PredictionRequest):
    """
    Make a prediction using the trained model
    
    - **features**: List of feature values for prediction
    """
    global current_model, model_metadata
    
    try:
        if current_model is None:
            raise HTTPException(status_code=400, detail="No model available. Please train a model first.")
        
        # Validate input features
        expected_features = model_metadata.get("input_features", 0)
        if len(request.features) != expected_features:
            raise HTTPException(
                status_code=400, 
                detail=f"Expected {expected_features} features, got {len(request.features)}"
            )
        
        # Prepare input data
        X_new = np.array([request.features], dtype=np.float32)
        
        # Validate input values
        if not np.isfinite(X_new).all():
            raise HTTPException(status_code=400, detail="All feature values must be finite numbers")
        
        # Make prediction
        api_logger.info(f"Making prediction with features: {request.features}")
        prediction = make_prediction(current_model, X_new)
        prediction_value = float(prediction[0][0])
        
        api_logger.info(f"Prediction result: {prediction_value}")
        
        return PredictionResponse(
            status="success",
            prediction=prediction_value,
            model_id=model_metadata["model_id"],
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_endpoint(
    file: UploadFile = File(..., description="CSV file with test data")
):
    """
    Evaluate the trained model on new test data
    
    - **file**: CSV file containing test data with same structure as training data
    """
    global current_model, model_metadata
    
    try:
        if current_model is None:
            raise HTTPException(status_code=400, detail="No model available. Please train a model first.")
        
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV file")
        
        # Read uploaded file
        contents = await file.read()
        csv_data = io.StringIO(contents.decode('utf-8'))
        
        # Load and preprocess data
        api_logger.info("Loading evaluation data")
        df = pd.read_csv(csv_data)
        df = preprocess_data(df)
        
        if df.empty:
            raise HTTPException(status_code=400, detail="No valid data after preprocessing")
        
        if df.shape[1] != model_metadata["input_features"] + 1:
            raise HTTPException(
                status_code=400, 
                detail=f"Data must have {model_metadata['input_features'] + 1} columns"
            )
        
        # Prepare test data
        X_test = df.iloc[:, :-1].values.astype(np.float32)
        y_test = df.iloc[:, -1].values.astype(np.float32)
        
        if len(X_test) < 1:
            raise HTTPException(status_code=400, detail="No test samples available")
        
        # Evaluate model
        api_logger.info(f"Evaluating model on {len(X_test)} samples")
        loss, mae = evaluate_model(current_model, X_test, y_test)
        
        api_logger.info(f"Evaluation results - Loss: {loss}, MAE: {mae}")
        
        return EvaluationResponse(
            status="success",
            model_id=model_metadata["model_id"],
            loss=loss,
            mae=mae,
            test_samples=len(X_test),
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"Evaluation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

@app.get("/model/info")
async def get_model_info():
    """Get information about the currently loaded model"""
    if current_model is None:
        raise HTTPException(status_code=404, detail="No model loaded")
    
    return {
        "status": "success",
        "model_metadata": model_metadata,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Run the FastAPI app
    uvicorn.run(
        "fastapi_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
