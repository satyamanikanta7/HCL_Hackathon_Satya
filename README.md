# Fraud Detection in Bank Transactions

This project demonstrates a simple end-to-end **Fraud Detection System** built with FastAPI and a Machine Learning model tested on the **Fraudulent Transaction Detection dataset from Kaggle**.  
The backend fetches recent transaction data from **Google Sheets**, applies a trained ML model, and flags suspicious transactions.  
Flagged transactions are logged and automatically trigger an **email notification** to the admin.

---

## 1. Project Overview

### Goal
Detect fraudulent transactions from Google Sheets data in real-time using a pre-trained ML model.

### Flow
1. Train the ML model using the Kaggle dataset and save it as `model.joblib`.  
2. The backend fetches transaction data from Google Sheets (acting as live bank transaction data).  
3. The ML model predicts fraud probability for each transaction.  
4. Transactions with a fraud probability above the threshold (e.g., 0.8) are marked as *Suspicious*.  
5. Admin receives an automatic email notification listing suspicious transactions.  

This setup simulates a practical **fraud detection pipeline** without complex user management or front-end dependencies.

---

## 2. Architecture Overview

             ┌──────────────────────────┐
             │   Google Sheet (Data)    │
             │ Transaction Records      │
             └──────────┬───────────────┘
                        │
                        ▼
            ┌──────────────────────────┐
            │ FastAPI Backend          │
            │ - Fetch Sheet Data       │
            │ - Predict Fraud Score    │
            │ - Flag Suspicious Txns   │
            │ - Send Email Alerts      │
            └──────────┬───────────────┘
                        │
                        ▼
             ┌──────────────────────────┐
             │ ML Model (model.joblib)  │
             │ Trained on Kaggle Data   │
             └──────────┬───────────────┘
                        │
                        ▼
             ┌──────────────────────────┐
             │ Auditor Dashboard        │
             │ - Send email notification│
             └──────────────────────────┘

---

## 3. Features

- Fetches transaction data from Google Sheets  
- Predicts fraud probability using a trained ML model  
- Flags suspicious transactions automatically  
- Sends email notifications to the admin for flagged entries  
- Optional web dashboard to view results  

---

## 4. Tech Stack

### Backend
- **FastAPI** – REST API development  
- **Requests / gspread** – fetch data from Google Sheets  
- **smtplib / FastAPI-Mail** – send email notifications  
- **Uvicorn** – run the backend server  

### Machine Learning
- **pandas**, **scikit-learn**, **joblib**  
- Trained using **Isolation Forest** (unsupervised anomaly detection)  
- Dataset: **Kaggle Credit Card Fraud Dataset**

### Database
- **CSV file** to store flagged transactions  

### External Integrations
- **Google Sheets API** – fetch transaction data  
- **SMTP (Gmail)** – send email alerts  

---

## 5. API Routes

| Method | Endpoint | Description |
|--------|-----------|-------------|
| GET | `/fetch-transactions` | Fetch all transactions from Google Sheet |
| GET | `/predict` | Run fraud prediction on all fetched transactions |
| GET | `/flagged` | Get list of flagged (suspicious) transactions |
| POST | `/notify-admin` | Send email notification for flagged transactions |

---

## 6. Backend Flow

1. Admin runs `/predict` endpoint manually or via a scheduled job.  
2. The FastAPI backend:
   - Pulls data from Google Sheets.  
   - Loads the trained model (`model.joblib`).  
   - Applies model predictions to compute fraud scores.  
   - Flags transactions above `ALERT_THRESHOLD`.  
3. Sends an email to the admin with flagged transactions.  
4. Optionally stores results in a local CSV file.  

---

## 7. Project Structure

```
fraud-detection/
│
├── backend/
│   ├── main.py                  # FastAPI entry point
│   ├── routes/
│   │   ├── transactions.py      # Fetch & predict routes
│   │   └── notify.py            # Email notification route
│   ├── services/
│   │   ├── sheets_service.py    # Google Sheets fetch logic
│   │   ├── model_service.py     # Load model & predict
│   │   └── notifier.py          # Email sending
│   ├── core/
│   │   ├── config.py            # Environment setup
│   │   └── utils.py             # Helper functions
│   ├── tests/                   # Unit test files
│   │   ├── test_api.py
│   │   ├── test_model_service.py
│   │   └── test_notifier.py
│   └── requirements.txt
│
├── ml_model/
│   ├── train_model.py           # Train Isolation Forest
│   ├── preprocess.py            # Data cleaning
│   └── model.joblib             # Saved trained model
│
└── README.md
```

## 8. Assumptions & Simplifications

This project is designed as a **functional prototype** to focus on the Machine Learning and anomaly detection logic rather than production-scale infrastructure.  
To keep implementation time-efficient and emphasize ML model development, the following assumptions and simplifications have been made:

1. **Data Source:**  
   - Transaction data is fetched from a **Google Sheet** instead of a real banking database.  
   - The sheet simulates live incoming transactions for testing anomaly detection.  

2. **User Management:**  
   - There is **no authentication or login system** implemented.  
   - It is assumed that a valid admin exists and receives alerts automatically.

3. **Infrastructure:**  
   - No message queues (e.g., Kafka, Celery) or cloud pipelines are used.  
   - All operations (fetch, predict, notify) are triggered manually or on request.

4. **Storage:**  
   - Flagged transactions are stored in a **local CSV file** instead of a relational database.  
   - This simplification makes the setup lightweight and easily portable.

5. **Notifications:**  
   - Alerts are sent using a **Gmail SMTP server** to demonstrate real-time notification.  
   - In production, this would be replaced by a secure email/notification microservice.

6. **Focus:**  
   - The project’s main focus is on the **ML component (Anomaly Detection)** — model training, evaluation, and integration with FastAPI.
   - The backend and integrations are intentionally kept simple to allow more time for model experimentation.

---

## 9. API Endpoints, Parameters, and Outputs

| Method | Endpoint | Parameters | Description | Example Output |
|--------|-----------|-------------|--------------|----------------|
| **GET** | `/fetch-transactions` | None | Fetches transaction data from the Google Sheet | `{ "transactions": [ { "Time": 0, "Amount": 200.0, ... }, ... ] }` |
| **GET** | `/predict` | None | Runs fraud prediction on all transactions fetched from the Google Sheet | `{ "transactions": [ { "Time": 0, "Amount": 200.0, "Fraud_Score": 0.82, "Flagged": true }, ... ] }` |
| **GET** | `/flagged` | None | Retrieves only the suspicious (flagged) transactions above the threshold | `{ "flagged_transactions": [ { "Amount": 950.5, "Fraud_Score": 0.91 }, ... ] }` |
| **POST** | `/notify-admin` | Optional JSON: `{ "subject": "Alert", "message": "Custom alert body" }` | Sends email notification to admin listing all flagged transactions | `{ "status": "Email sent successfully", "count": 5 }` |

**Note:**  
- The `/predict` endpoint internally calls the Google Sheets fetch function and the ML model prediction.  
- The `Fraud_Score` represents the anomaly score or probability of fraud, depending on the model type.  
- Threshold (`ALERT_THRESHOLD`, default = 0.8) can be modified in `.env`.

---

## 10. Quick Start

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd fraud-detection
```

### Step 2: Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 3: Configure Environment Variables
Create a `.env` file in the `backend/` directory:

```env
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_API_CREDENTIALS_PATH=credentials.json
MODEL_PATH=ml_model/model.joblib
ALERT_THRESHOLD=0.8
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=youremail@gmail.com
SMTP_PASSWORD=yourpassword
ADMIN_EMAIL=admin@example.com
```

### Step 4: Start the Backend Server
```bash
uvicorn backend.main:app --reload
```

### Step 5: Access API Documentation
Visit:  
`http://localhost:8000/docs`

---

## 11. Future Enhancements

- Schedule automatic prediction (cron job or Celery)  
- Add model explainability (SHAP/LIME)  
- Store flagged results in PostgreSQL  
- Add admin login & role-based access  
- Deploy using Docker Compose on Render or AWS  

---

## 12. Author

**Name:** Potti Satya Manikanta 
**Email:** pottisatyamanikanta@gmail.com  
**Institution:** Indian Institute of Technology Kharagpur
