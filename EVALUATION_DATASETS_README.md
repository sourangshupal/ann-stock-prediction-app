# 📊 Evaluation Datasets for AAPL Stock Prediction API

I've created evaluation datasets from your AAPL.csv file that you can use to test the FastAPI endpoints through Swagger UI.

## 📁 Created Files

### 1. **`data/AAPL_training.csv`** (1,131 rows)
- **Purpose**: Training dataset
- **Date Range**: 2019-01-02 to 2023-06-29
- **Use**: Upload this file to `/train` endpoint

### 2. **`data/AAPL_evaluation.csv`** (378 rows)
- **Purpose**: Full evaluation dataset
- **Date Range**: 2023-06-30 to 2024-12-30
- **Use**: Upload this file to `/evaluate` endpoint

### 3. **`data/AAPL_test_small.csv`** (38 rows)
- **Purpose**: Quick testing (every 10th row from evaluation data)
- **Date Range**: 2023-06-30 to 2024-12-18
- **Use**: Upload this file to `/evaluate` endpoint for faster testing

## 🎯 Data Structure

All datasets have the same structure:
```csv
Date,Close,High,Low,Open,Volume
2023-06-30,192.047,192.552,189.364,189.730,85069600
2023-07-03,190.552,191.958,189.859,191.859,31458200
...
```

**After preprocessing:**
- **Date column** will be automatically removed
- **Features (X)**: Close, High, Low, Open (4 features)
- **Target (y)**: Volume (what the model predicts)

## 🚀 Testing Workflow with Swagger UI

### Step 1: Start FastAPI Server
```bash
# Windows
build.bat api

# Access Swagger UI at: http://localhost:8000/docs
```

### Step 2: Train Model
1. Go to **Swagger UI**: http://localhost:8000/docs
2. Click **`POST /train`**
3. Click **"Try it out"**
4. **Upload file**: `data/AAPL_training.csv`
5. **Set parameters**:
   - epochs: `20` (for quick testing)
   - batch_size: `32`
   - test_split: `0.2`
6. Click **"Execute"**

**Expected Response:**
```json
{
  "status": "success",
  "message": "Model trained successfully",
  "model_id": "model_20231203_143022",
  "training_time": 25.67,
  "data_shape": [1131, 5],
  "train_samples": 904,
  "test_samples": 227,
  "loss": 0.0234,
  "mae": 0.1123
}
```

### Step 3: Make Predictions
1. Click **`POST /predict`**
2. Click **"Try it out"**
3. **Enter sample features** (based on recent AAPL data):

**Sample 1 - Recent High Price:**
```json
{
  "features": [251.55, 253.67, 247.14, 247.45]
}
```

**Sample 2 - Mid-Range Price:**
```json
{
  "features": [220.85, 224.45, 219.00, 220.14]
}
```

**Sample 3 - Lower Price Range:**
```json
{
  "features": [169.73, 171.01, 168.60, 169.10]
}
```

4. Click **"Execute"**

**Expected Response:**
```json
{
  "status": "success",
  "prediction": 56774100.0,
  "model_id": "model_20231203_143022",
  "timestamp": "2023-12-03T14:35:22.123456"
}
```

### Step 4: Evaluate Model
1. Click **`POST /evaluate`**
2. Click **"Try it out"**
3. **Upload evaluation file**:
   - For **quick test**: `data/AAPL_test_small.csv`
   - For **full evaluation**: `data/AAPL_evaluation.csv`
4. Click **"Execute"**

**Expected Response:**
```json
{
  "status": "success",
  "model_id": "model_20231203_143022",
  "loss": 0.0198,
  "mae": 0.1045,
  "test_samples": 38,
  "timestamp": "2023-12-03T14:40:15.789012"
}
```

## 📈 Sample Prediction Values

Based on the AAPL evaluation data, here are realistic feature combinations:

### High Price Period (2024 Recent)
```json
{"features": [251.55, 253.67, 247.14, 247.45]}
```
*Expected Volume: ~50-60M*

### Medium Price Period (2024 Mid-Year)
```json
{"features": [220.85, 224.45, 219.00, 220.14]}
```
*Expected Volume: ~40-50M*

### Lower Price Period (2024 Early)
```json
{"features": [169.73, 171.01, 168.60, 169.10]}
```
*Expected Volume: ~90-100M*

### Volatile Period
```json
{"features": [213.74, 215.74, 210.62, 213.24]}
```
*Expected Volume: ~95-100M*

## 🔍 Understanding the Results

### Training Results
- **Loss**: Lower is better (typically 0.01-0.05)
- **MAE**: Mean Absolute Error in volume prediction
- **Training Time**: Should be 15-30 seconds for 20 epochs

### Prediction Results
- **Volume predictions** typically range from 25M to 150M
- **Higher prices** often correlate with **lower volume**
- **Lower prices** often correlate with **higher volume** (more trading activity)

### Evaluation Results
- **Loss**: How well the model performs on unseen data
- **MAE**: Average prediction error in volume units
- **Test Samples**: Number of data points evaluated

## 🎯 Quick Test Commands

### Using curl (Alternative to Swagger UI)

**Train Model:**
```bash
curl -X POST "http://localhost:8000/train" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/AAPL_training.csv" \
  -F "epochs=20" \
  -F "batch_size=32"
```

**Make Prediction:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [220.85, 224.45, 219.00, 220.14]}'
```

**Evaluate Model:**
```bash
curl -X POST "http://localhost:8000/evaluate" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/AAPL_test_small.csv"
```

## 📊 Data Statistics

### Training Data (AAPL_training.csv)
- **Rows**: 1,131
- **Date Range**: 2019-01-02 to 2023-06-29
- **Price Range**: ~$33-$194
- **Volume Range**: ~28M-400M

### Evaluation Data (AAPL_evaluation.csv)
- **Rows**: 378
- **Date Range**: 2023-06-30 to 2024-12-30
- **Price Range**: ~$164-$259
- **Volume Range**: ~23M-318M

### Small Test Data (AAPL_test_small.csv)
- **Rows**: 38
- **Date Range**: 2023-06-30 to 2024-12-18
- **Purpose**: Quick API testing

## 🚦 Expected Performance

With the AAPL datasets, you should expect:
- **Training Time**: 15-30 seconds (20 epochs)
- **Loss**: 0.01-0.05 (lower is better)
- **MAE**: 5M-15M volume units
- **Prediction Range**: 25M-150M volume

## 🔧 Troubleshooting

### Common Issues

**1. Training takes too long**
- Reduce epochs to 10-15
- Use smaller batch_size (16)

**2. High loss/MAE values**
- Try more epochs (50-100)
- Check data quality

**3. Unrealistic predictions**
- Ensure feature values are in realistic ranges
- Check that model was trained successfully

## 🎉 Ready to Test!

1. **Start API**: `build.bat api`
2. **Open Swagger**: http://localhost:8000/docs
3. **Train with**: `data/AAPL_training.csv`
4. **Predict with**: Sample feature values above
5. **Evaluate with**: `data/AAPL_test_small.csv`

The evaluation datasets are now ready for comprehensive testing of your FastAPI endpoints! 🚀
