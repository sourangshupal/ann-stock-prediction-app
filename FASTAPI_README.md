# 🚀 FastAPI REST API for ANN Stock Prediction

This FastAPI server provides REST API endpoints for training, prediction, and evaluation of the ANN stock prediction model. Test all endpoints through the interactive Swagger UI!

## 📋 API Endpoints

### 🏠 **Root & Health**
- `GET /` - API information and status
- `GET /health` - Health check endpoint
- `GET /docs` - **Swagger UI** (Interactive API documentation)
- `GET /redoc` - ReDoc documentation

### 🎯 **Core Functionality**
- `POST /train` - Train a new model with uploaded CSV data
- `POST /predict` - Make predictions using the trained model
- `POST /evaluate` - Evaluate model performance on test data
- `GET /model/info` - Get information about the current model

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

```bash
# Start FastAPI server
docker-compose up ann-stock-api

# Access Swagger UI at: http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python fastapi_app.py

# Or using uvicorn directly
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```

## 🌐 Access Points

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health

## 📊 API Usage Examples

### 1. **Train Model** (`POST /train`)

**Using Swagger UI:**
1. Go to http://localhost:8000/docs
2. Click on `POST /train`
3. Click "Try it out"
4. Upload your CSV file
5. Set parameters (epochs, batch_size, test_split)
6. Click "Execute"

**Using curl:**
```bash
curl -X POST "http://localhost:8000/train" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/sample_stock_data.csv" \
  -F "epochs=50" \
  -F "batch_size=32" \
  -F "test_split=0.2"
```

**Response:**
```json
{
  "status": "success",
  "message": "Model trained successfully",
  "model_id": "model_20231203_143022",
  "training_time": 15.67,
  "data_shape": [15, 5],
  "train_samples": 12,
  "test_samples": 3,
  "loss": 0.0234,
  "mae": 0.1123
}
```

### 2. **Make Prediction** (`POST /predict`)

**Using Swagger UI:**
1. Go to http://localhost:8000/docs
2. Click on `POST /predict`
3. Click "Try it out"
4. Enter feature values in JSON format
5. Click "Execute"

**Request Body:**
```json
{
  "features": [100.50, 101.25, 99.80, 100.75]
}
```

**Using curl:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [100.50, 101.25, 99.80, 100.75]}'
```

**Response:**
```json
{
  "status": "success",
  "prediction": 1250000.75,
  "model_id": "model_20231203_143022",
  "timestamp": "2023-12-03T14:35:22.123456"
}
```

### 3. **Evaluate Model** (`POST /evaluate`)

**Using Swagger UI:**
1. Go to http://localhost:8000/docs
2. Click on `POST /evaluate`
3. Click "Try it out"
4. Upload test CSV file
5. Click "Execute"

**Using curl:**
```bash
curl -X POST "http://localhost:8000/evaluate" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/test_data.csv"
```

**Response:**
```json
{
  "status": "success",
  "model_id": "model_20231203_143022",
  "loss": 0.0198,
  "mae": 0.1045,
  "test_samples": 10,
  "timestamp": "2023-12-03T14:40:15.789012"
}
```

### 4. **Get Model Info** (`GET /model/info`)

**Using Swagger UI:**
1. Go to http://localhost:8000/docs
2. Click on `GET /model/info`
3. Click "Try it out"
4. Click "Execute"

**Response:**
```json
{
  "status": "success",
  "model_metadata": {
    "model_id": "model_20231203_143022",
    "created_at": "2023-12-03T14:30:22.123456",
    "input_features": 4,
    "training_samples": 12,
    "test_samples": 3,
    "epochs": 50,
    "batch_size": 32,
    "loss": 0.0234,
    "mae": 0.1123
  },
  "timestamp": "2023-12-03T14:45:30.456789"
}
```

## 🧪 Testing the API

### Automated Testing

```bash
# Run the test script
python test_fastapi.py
```

This will test all endpoints and provide a comprehensive report.

### Manual Testing with Sample Data

1. **Start the API server**
2. **Go to Swagger UI**: http://localhost:8000/docs
3. **Train a model**:
   - Use `POST /train`
   - Upload `data/sample_stock_data.csv`
   - Set epochs=10 for quick testing
4. **Make a prediction**:
   - Use `POST /predict`
   - Input: `{"features": [100.50, 101.25, 99.80, 100.75]}`
5. **Evaluate the model**:
   - Use `POST /evaluate`
   - Upload the same or different CSV file

## 📁 Data Format

### Training/Evaluation Data (CSV)
```csv
Date,Open,High,Low,Close,Volume
2023-01-01,100.0,105.0,95.0,102.0,1000000
2023-01-02,101.0,106.0,96.0,103.0,1100000
...
```

**Notes:**
- Date column will be automatically removed
- Last column is treated as the target variable
- All other columns are features
- Data will be automatically preprocessed

### Prediction Input
```json
{
  "features": [price, close, high, low, open]
}
```

**Example for AAPL data:**
- Price: 100.50
- Close: 101.25  
- High: 99.80
- Low: 100.75

## 🐳 Docker Services

### Production Services
```bash
# Start both Streamlit and FastAPI
docker-compose up

# Start only FastAPI
docker-compose up ann-stock-api

# Start only Streamlit
docker-compose up ann-stock-app
```

### Development Services
```bash
# Start FastAPI in development mode (with hot reload)
docker-compose --profile dev up ann-stock-api-dev

# Access at: http://localhost:8001/docs
```

## 🔧 Configuration

### Environment Variables
- `PYTHONUNBUFFERED=1` - Unbuffered Python output
- `TF_CPP_MIN_LOG_LEVEL=2` - TensorFlow logging level

### API Parameters
- **epochs**: 1-1000 (default: 50)
- **batch_size**: 1-512 (default: 32)
- **test_split**: 0.1-0.5 (default: 0.2)

## 📊 Response Codes

- **200**: Success
- **400**: Bad Request (invalid input, no model loaded, etc.)
- **404**: Not Found (model info when no model loaded)
- **422**: Validation Error (invalid request format)
- **500**: Internal Server Error

## 🔍 Monitoring & Logs

### Health Monitoring
```bash
# Check API health
curl http://localhost:8000/health

# Check container health
docker ps
```

### View Logs
```bash
# API logs
docker-compose logs ann-stock-api

# Application logs
tail -f logs/fastapi.log
```

## 🚦 Production Considerations

1. **Security**: Add authentication/authorization
2. **Rate Limiting**: Implement request rate limiting
3. **Model Persistence**: Save/load models to/from disk
4. **Monitoring**: Add metrics and monitoring
5. **Scaling**: Use multiple workers with Gunicorn

## 🆘 Troubleshooting

### Common Issues

**1. API not responding**
```bash
# Check if container is running
docker ps | grep ann-stock-prediction-api

# Check logs
docker-compose logs ann-stock-api
```

**2. Training fails**
- Ensure CSV has proper format
- Check data has enough rows (minimum 10)
- Verify all columns are numeric (except Date)

**3. Prediction fails**
- Train a model first using `/train`
- Ensure feature count matches training data
- Check all feature values are numeric

**4. Port conflicts**
```bash
# Use different port
docker run -p 8080:8000 ann-stock-api
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Swagger UI Guide](https://swagger.io/tools/swagger-ui/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

---

🎉 **Ready to test!** Go to http://localhost:8000/docs and start exploring the API!
