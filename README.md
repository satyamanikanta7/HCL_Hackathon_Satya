# Fraud Detection System

A fraud detection system built with FastAPI and machine learning for identifying suspicious bank transactions.

## Overview

This system fetches transaction data from Google Sheets, applies a trained ML model to detect fraud, and sends email notifications for flagged transactions.

## Architecture

```
Google Sheets → FastAPI Backend → ML Model → Email Notifications
```

## Features

- Transaction data fetching from Google Sheets
- Machine learning-based fraud detection
- Automatic email alerts for suspicious transactions
- REST API for system interaction

## Tech Stack

- **Backend**: FastAPI, Python
- **ML**: scikit-learn, pandas, numpy
- **Data**: Google Sheets API
- **Notifications**: SMTP email

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI application
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   ├── models/              # Data models
│   ├── schemas/             # Pydantic schemas
│   ├── core/                # Configuration
│   └── tests/               # Test files
├── ml_model/
│   ├── train_model.py       # Model training
│   └── model.joblib         # Trained model
└── requirements.txt
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/fraud/upload-csv` | Upload CSV and run fraud detection |
| GET | `/api/fraud/flagged` | Get flagged transactions |
| POST | `/api/fraud/notify-admin` | Send email notification |

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```env
MODEL_PATH=ml_model/model.joblib
ALERT_THRESHOLD=0.8
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_password
ADMIN_EMAIL=admin@example.com
```

3. Start the server:
```bash
uvicorn backend.main:app --reload
```

4. Access API documentation at `http://localhost:8000/docs`

## Testing

Run tests from the backend directory:
```bash
cd backend
python tests/simple_test_runner.py
```

## Author

Potti Satya Manikanta  
Email: pottisatyamanikanta@gmail.com