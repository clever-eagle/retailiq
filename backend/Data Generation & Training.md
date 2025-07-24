# Data Generation & Training

---

## 1. `large_market_basket_data.csv`

- **What it contains:**  
  CSV file filled with sales transactions that mimic real-world data.
- **When is this file used:**  
  For training, testing, and analysis in the backend; as input for model training.
- **How does the file work:**  
  Uploaded to the backend, read by scripts, and fed to the models for training.

---

- **What it contains:**  
  Python script for ensuring the system's initial state has no data loaded and displays a summary of the output.
- **How does the file work:**
  - Uploads the CSV data file to the backend.
  - Validates that the upload was successful and confirms the backend processed the file by fetching the output.
  - Ensures backend endpoints work as expected:
    - `/data-summary`
    - `/upload-data`
    - `/current-analysis`

---

## 3. `sample_data_generator.py`

- **What it contains:**  
  Python script for generating synthetic test data that mimics the structure of `large_market_basket_data.csv`.
- **What is the file used for:**
  - Processes the generated synthetic test data.
  - Feeds it to the ML model to retrain.
  - Validates the ML workflow and pipeline:
    - Ensures the model can be retrained using new synthetic data.
    - Ensures data processing steps (cleaning, formatting, feature extraction) work as expected.
    - Confirms model training completes without errors and produces results.
    - Checks that backend analysis functions (such as predictions or summaries) return correct outputs after retraining.
  - In short, it ensures the entire process—from data generation to model training to producing analysis results—works correctly and reliably.

---

## 4. `test_market_basket.py`

- **What it contains:**  
  Python script for testing market basket analysis and producing results.
- **How does it work:**
  - Sends a POST request to the `/market-basket-analysis` endpoint with parameters for minimum support and confidence.
  - Receives the response, which contains support & confidence for association rules.
  - Prints the structure of the first rule and the total number of rules found.
  - Reports errors if the request fails.
