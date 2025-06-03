# 📊 Sample Prediction Data for AAPL Stock Model

Based on your AAPL.csv data structure, here are sample inputs you can use for making predictions in the Streamlit app.

## 📋 Data Structure
After preprocessing your AAPL.csv, the model expects **5 features** in this order:
1. **Price** (Close price)
2. **Close** (Close price) 
3. **High** (High price)
4. **Low** (Low price)
5. **Open** (Open price)

The model will predict: **Volume** (trading volume)

## 🎯 Sample Prediction Inputs

### Sample 1: Recent AAPL-like values
```
37.62, 37.84, 36.74, 36.90, 148158800
```
**Expected prediction:** Around 148-150 million volume

### Sample 2: Higher price range
```
125.75, 126.41, 123.46, 124.29, 98208600
```
**Expected prediction:** Around 95-100 million volume

### Sample 3: Mid-range values
```
78.89, 79.27, 78.32, 78.83, 104491200
```
**Expected prediction:** Around 100-105 million volume

### Sample 4: Lower price range
```
55.56, 61.03, 55.26, 59.91, 401693200
```
**Expected prediction:** Around 350-400 million volume (high volatility period)

### Sample 5: Stable period
```
113.73, 114.61, 113.37, 113.71, 46691300
```
**Expected prediction:** Around 45-50 million volume

## 🔧 How to Use in Streamlit

1. **Upload your AAPL.csv file** to train the model
2. **Wait for training to complete** 
3. **In the prediction section**, enter one of the sample inputs above
4. **Click "Predict"** to see the predicted volume

## 📝 Format Notes

- **Comma-separated values** (no spaces after commas work too)
- **Decimal numbers** are fine (e.g., 37.62)
- **Order matters** - make sure to follow: Price, Close, High, Low, Open
- **Volume is predicted** - don't include it in your input

## 🎲 Try These Variations

### Conservative Trading Day:
```
120.50, 121.00, 119.80, 120.25, 75000000
```

### High Volatility Day:
```
95.20, 98.50, 92.10, 94.80, 250000000
```

### Steady Growth:
```
110.25, 111.50, 109.75, 110.00, 85000000
```

### Market Correction:
```
85.60, 88.20, 82.40, 87.15, 180000000
```

## 💡 Tips for Best Results

1. **Use realistic price ranges** - AAPL typically trades between $30-130 in your dataset
2. **Keep price relationships logical** - High should be ≥ Close/Open, Low should be ≤ Close/Open  
3. **Price and Close are often similar** - they represent the same metric in your data
4. **Volume varies widely** - from ~45M to ~400M+ depending on market conditions

## 🚀 Quick Test

Copy and paste this into the Streamlit prediction box:
```
100.50, 101.25, 99.80, 100.75
```

This represents a stock trading around $100-101 with normal daily fluctuation.
