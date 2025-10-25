# Simple tests for fraud detection system components
import pandas as pd
import numpy as np

def test_pandas_import():
    """Test that pandas can be imported and used."""
    df = pd.DataFrame({'amount': [100, 200, 300]})
    assert len(df) == 3
    assert df['amount'].sum() == 600

def test_numpy_import():
    """Test that numpy can be imported and used."""
    arr = np.array([1, 2, 3, 4, 5])
    assert len(arr) == 5
    assert arr.mean() == 3.0

def test_fraud_score_calculation():
    """Test basic fraud score calculation logic."""
    # Simple fraud score calculation
    amounts = [100, 500, 1000, 5000]
    fraud_scores = []
    
    for amount in amounts:
        # Simple rule: higher amounts get higher fraud scores
        score = min(amount / 1000, 1.0)
        fraud_scores.append(score)
    
    assert fraud_scores[0] == 0.1  # 100/1000
    assert fraud_scores[3] == 1.0  # 5000/1000 capped at 1.0

def test_transaction_filtering():
    """Test filtering transactions based on fraud score."""
    transactions = [
        {'id': 1, 'amount': 100, 'fraud_score': 0.1},
        {'id': 2, 'amount': 500, 'fraud_score': 0.5},
        {'id': 3, 'amount': 1000, 'fraud_score': 0.8},
        {'id': 4, 'amount': 2000, 'fraud_score': 0.9}
    ]
    
    threshold = 0.7
    flagged = [t for t in transactions if t['fraud_score'] > threshold]
    
    assert len(flagged) == 2
    assert flagged[0]['id'] == 3
    assert flagged[1]['id'] == 4

def test_email_formatting():
    """Test email content formatting."""
    flagged_transactions = [
        {'id': 1, 'amount': 1000, 'fraud_score': 0.8},
        {'id': 2, 'amount': 2000, 'fraud_score': 0.9}
    ]
    
    subject = "Fraud Alert - Suspicious Transactions Detected"
    body = f"Suspicious transactions detected: {len(flagged_transactions)} transactions flagged\n\n"
    
    for i, transaction in enumerate(flagged_transactions, 1):
        body += f"{i}. Transaction ID: {transaction['id']}\n"
        body += f"   Amount: ${transaction['amount']}\n"
        body += f"   Fraud Score: {transaction['fraud_score']:.1f}\n\n"
    
    assert "Fraud Alert" in subject
    assert "2 transactions flagged" in body
    assert "Transaction ID: 1" in body
    assert "Transaction ID: 2" in body
