import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.core.config import settings

def send_fraud_alert(flagged_transactions: list[dict]) -> bool:
    """Send formatted fraud alert email."""
    if not flagged_transactions:
        return False
    
    subject = "Fraud Alert - Suspicious Transactions Detected"
    
    body = "FRAUD ALERT\n\n"
    body += f"Suspicious transactions detected: {len(flagged_transactions)} transactions flagged\n\n"
    body += "Transaction Details:\n"
    body += "-" * 50 + "\n"
    
    for i, transaction in enumerate(flagged_transactions, 1):
        body += f"{i}. Transaction ID: {transaction.get('ID', 'N/A')}\n"
        body += f"   Customer: {transaction.get('Name', 'N/A')}\n"
        body += f"   Time: {transaction.get('Time', 'N/A')}\n"
        body += f"   Fraud Score: {transaction.get('fraud_score', 'N/A'):.4f}\n"
        body += f"   Amount: ${transaction.get('Amount', 'N/A')}\n"
        body += "\n"
    
    body += "\nPlease review these transactions immediately.\n"
    body += "This is an automated alert from the Fraud Detection System."
    
    try:
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_USER
        msg["To"] = settings.ADMIN_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"Email sent successfully to {settings.ADMIN_EMAIL}")
        return True
        
    except Exception as e:
        print(f"Email send failed: {e}")
        return False
