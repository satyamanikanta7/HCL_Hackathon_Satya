# Fraud Detection System

A comprehensive fraud detection system built with FastAPI and machine learning for identifying suspicious bank transactions using real-world datasets.

## Overview

This system processes transaction data through a complete ML pipeline: data ingestion from CSV upload, fraud detection using trained models, and automated alerting for suspicious activities.

## Dataset Information

### Kaggle Credit Card Fraud Detection Dataset
- **Source**: [Kaggle Credit Card Fraud Detection](https://www.kaggle.com/mlg-ulb/creditcardfraud)
- **Features**: 30 numerical features (PCA-transformed for privacy)
- **Time Period**: Transactions over 2 days in September 2013
- **Privacy**: All features anonymized using PCA transformation

### Dataset Features
- `Time`: Seconds elapsed between transaction and first transaction
- `Amount`: Transaction amount
- `V1-V28`: PCA-transformed features (anonymized)
- `Class`: Target variable (0 = normal, 1 = fraud)

## Data Flow Architecture

```

│   Kaggle Data   │───▶│  Model Training │───▶│  Trained Model │
│   (284K records)│    │  (Isolation     │    │  (model.joblib) │
│                 │    │   Forest)       │    │                 │

                                                         │
                                                         ▼

│  Google Sheets  │───▶│  FastAPI        │───▶│  ML Prediction  │
│  (Live Data)    │    │  Backend        │    │  & Scoring      │

                                                         │
                                                         ▼

│  Email Alerts   │◀───│  Flagged       │◀───│  Fraud Detection │
│  (SMTP)         │    │  Transactions   │    │  Results         │

```

## System Flow

1. **Data Ingestion**: Transaction data fetched from Google Sheets
2. **Preprocessing**: Data cleaned and normalized using trained scaler
3. **ML Prediction**: Isolation Forest model predicts fraud probability
4. **Threshold Filtering**: Transactions above threshold flagged as suspicious
5. **Alert Generation**: Email notifications sent to administrators

## Machine Learning Model

### Algorithm: Isolation Forest
- **Type**: Unsupervised anomaly detection
- **Advantages**: 
  - No need for labeled fraud data during inference
  - Handles high-dimensional data well
  - Fast training and prediction
- **Contamination Rate**: 0.01 (1% expected fraud rate)
- **Random State**: 42 (for reproducibility)

### Model Performance
- **Training Data**: 284,807 transactions from Kaggle
- **Features Used**: All 30 PCA-transformed features + Amount
- **Validation**: Cross-validation on time-based splits
- **Threshold**: Configurable (default: 0.8)

## Features

- **Real-time Processing**: Live transaction data from Google Sheets
- **ML-powered Detection**: Trained on real fraud dataset
- **Automated Alerts**: Email notifications for suspicious activities
- **REST API**: Complete API for system integration

## Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **ML Framework**: scikit-learn, pandas, numpy
- **Data Storage**: Google Sheets API, CSV files
- **Notifications**: SMTP (Gmail), email-validator
- **Authentication**: JWT tokens, bcrypt
- **Database**: SQLAlchemy (SQLite)
- **Testing**: pytest, httpx

## Project Structure

```
├── backend/
│   ├── main.py                  # FastAPI application entry point
│   ├── routes/
│   │   ├── api_router.py        # Main API router
│   │   ├── transactions.py      # Transaction endpoints
│   │   ├── auth.py             # Authentication endpoints
│   │   └── deps.py             # Dependencies
│   ├── services/
│   │   ├── auditor_service.py   # Main fraud detection service
│   │   ├── model_service.py     # ML model operations
│   │   └── notifier.py         # Email notification service
│   ├── models/
│   │   └── user.py             # User data models
│   ├── schemas/
│   │   ├── fraud.py            # Fraud detection schemas
│   │   └── user.py             # User schemas
│   ├── core/
│   │   ├── config.py           # Configuration settings
│   │   └── security.py         # Security utilities
│   ├── db/
│   │   ├── base.py             # Database base
│   │   ├── session.py          # Database session
│   │   └── init_db.py          # Database initialization
│   └── tests/                  # Test files
├── ml_model/
│   ├── train_model.py          # Model training script
│   ├── model.joblib            # Trained model file
│   ├── scaler.joblib           # Data scaler
│   └── Anamoly Detection.ipynb # Jupyter notebook for analysis
├── requirements.txt             # Python dependencies
├── fraud_detection.db          # SQLite database
├── flagged_transactions.csv    # Audit log
└── audit_log.csv              # System audit log
```

## API Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/fraud/upload-csv` | Upload CSV file and run fraud detection | Required |
| GET | `/api/fraud/flagged` | Retrieve flagged suspicious transactions | Required |
| POST | `/api/fraud/notify-admin` | Send email notification to admin | Required |
| POST | `/api/auth/login` | User authentication | None |
| POST | `/api/auth/register` | User registration | None |
| GET | `/health` | System health check | None |

## Environment Configuration

Create a `.env` file in the project root:

```env
# Application Settings
APP_NAME=Fraud Detection System
DEBUG=True

# Model Configuration
MODEL_PATH=ml_model/model.joblib
SCALER_PATH=ml_model/scaler.joblib
ALERT_THRESHOLD=0.8

# Database
DATABASE_URL=sqlite:///./fraud_detection.db

# Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ADMIN_EMAIL=admin@example.com

# Google Sheets (Optional)
GOOGLE_SHEET_ID=your_sheet_id
GOOGLE_API_CREDENTIALS_PATH=credentials.json
```

## Installation & Setup

1. **Clone Repository**:
```bash
git clone <repository-url>
cd HCL_Hackathon_Satya
```

2. **Create Virtual Environment**:
```bash
python -m venv .venv
source .venv/bin/activate  
```

3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

4. **Initialize Database**:
```bash
python backend/db/init_db.py
```

5. **Train Model** (if not already trained):
```bash
python ml_model/train_model.py
```

6. **Configure Environment**:
```bash
cp .env.example .env
```

7. **Start Application**:
```bash
uvicorn backend.main:app --reload
```

8. **Access Documentation**:
   - API Docs: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

## Author

**Potti Satya Manikanta**  
Email: pottisatyamanikanta@gmail.com  
Institution: Indian Institute of Technology Kharagpur