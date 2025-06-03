# 📈 ANN Stock Prediction App

Welcome to the ANN Stock Prediction App! This project provides a modular, well-logged solution for predicting stock prices using an Artificial Neural Network (ANN). You can use a beautiful Streamlit web interface or a command-line interface (CLI) for local execution.

---

## 🚀 Features
- Modular codebase for easy maintenance
- Logging in every component (data prep, training, evaluation, prediction)
- Streamlit webapp for interactive use
- CLI for quick terminal-based workflows
- Easy setup and extensibility

---

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ann-stock-prediction-app
   ```

2. **Install dependencies**
   Ensure you have Python 3.8+ and pip installed.
   ```bash
   pip install -r requirements.txt
   ```

---

## 🌐 Running the Streamlit Web App

1. **Start the app**
   ```bash
   streamlit run app.py
   ```
2. **Open your browser**
   - The app will open automatically, or visit [http://localhost:8501](http://localhost:8501)
3. **Upload your stock data CSV**
   - The last column should be the target variable (e.g., closing price)
4. **Train, evaluate, and predict**
   - Use the UI to train the model and make predictions interactively

---

## 🖥️ Running from the Command Line (CLI)

1. **Train, evaluate, and predict in one go:**
   ```bash
   python cli.py --data path/to/your/data.csv --epochs 50 --batch_size 32 --predict "1.2,3.4,5.6,7.8"
   ```
   - `--data`: Path to your CSV file
   - `--epochs`: (Optional) Number of training epochs (default: 50)
   - `--batch_size`: (Optional) Batch size (default: 32)
   - `--predict`: (Optional) Comma-separated feature values for prediction

2. **Example output:**
   ```
   Evaluation Results - Loss: 0.0123, MAE: 0.0890
   Predicted value: 123.45
   ```

---

## 📂 Project Structure

```
ann-stock-prediction-app/
├── app.py            # Streamlit webapp
├── cli.py            # Command-line interface
├── data_prep.py      # Data loading & preprocessing
├── model.py          # ANN model, training, evaluation
├── predict.py        # Prediction logic
├── logger.py         # Logging setup
├── requirements.txt  # Python dependencies
├── logs/             # Log files
└── README.md         # Project documentation
```

---

## 📝 Notes
- Make sure your CSV data is clean and the last column is the target for prediction.
- All logs are saved in the `logs/` directory for debugging and traceability.
- You can extend the ANN architecture or add new features as needed.

---

## 🙌 Contributing
Pull requests and suggestions are welcome! Feel free to fork the repo and submit improvements.

---

## 📧 Contact
For questions or support, please open an issue or contact the maintainer.

---

Enjoy predicting stocks! 🚀📊
