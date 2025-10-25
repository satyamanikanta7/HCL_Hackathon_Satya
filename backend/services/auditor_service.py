import pandas as pd
import os
from datetime import datetime
from typing import Dict
from backend.services.model_service import predict
from backend.services.notifier import send_fraud_alert

class AuditorDashboardService:
    """Service for auditor operations."""
    
    def __init__(self):
        self.flagged_file = "flagged_transactions.csv"
        self.audit_log_file = "audit_log.csv"
    
    def process_transactions(self, df: pd.DataFrame, user_email: str = "system") -> Dict:
        """Process transactions and return comprehensive results."""
        try:
            # Run fraud detection
            result_df = predict(df)
            
            # Save results
            result_df.to_csv(self.flagged_file, index=False)
            
            # Get flagged transactions
            flagged_df = result_df[result_df["flagged"] == True]
            
            # Log the audit action
            self._log_audit_action("transaction_scan", f"Processed {len(result_df)} transactions, {len(flagged_df)} flagged", user_email)
            
            return {
                "total_transactions": len(result_df),
                "flagged_count": len(flagged_df),
                "flagged": flagged_df.to_dict(orient="records"),
                "status": "success"
            }
            
        except Exception as e:
            self._log_audit_action("transaction_scan", f"Error: {str(e)}", user_email)
            raise e
    
    def get_flagged_transactions(self) -> Dict:
        """Get all flagged transactions."""
        try:
            if not os.path.exists(self.flagged_file):
                return {"flagged_transactions": []}
            
            df = pd.read_csv(self.flagged_file)
            flagged_df = df[df["flagged"] == True]
            
            return {"flagged_transactions": flagged_df.to_dict(orient="records")}
            
        except Exception as e:
            raise e
    
    def send_notification(self) -> Dict:
        """Send notification to admin about flagged transactions."""
        try:
            flagged_data = self.get_flagged_transactions()
            flagged_transactions = flagged_data["flagged_transactions"]
            
            if not flagged_transactions:
                return {
                    "status": "no_flagged_transactions",
                    "count": 0,
                    "message": "No suspicious transactions found"
                }
            
            # Send email notification
            success = send_fraud_alert(flagged_transactions)
            
            if success:
                self._log_audit_action("notification_sent", f"Sent alert for {len(flagged_transactions)} transactions", "system")
                return {
                    "status": "Email sent successfully",
                    "count": len(flagged_transactions),
                    "message": f"Alert sent for {len(flagged_transactions)} suspicious transactions"
                }
            else:
                self._log_audit_action("notification_failed", "Failed to send email alert", "error")
                return {
                    "status": "Email send failed",
                    "count": len(flagged_transactions),
                    "message": "Failed to send email notification"
                }
                
        except Exception as e:
            self._log_audit_action("notification_error", f"Error: {str(e)}", "error")
            raise e
    
    def _log_audit_action(self, action: str, details: str, user: str = "system"):
        """Log audit actions."""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "details": details,
                "status": "success",
                "user": user
            }
            
            if os.path.exists(self.audit_log_file):
                df = pd.read_csv(self.audit_log_file)
                df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
            else:
                df = pd.DataFrame([log_entry])
            
            df.to_csv(self.audit_log_file, index=False)
            
        except Exception as e:
            print(f"Failed to log audit action: {e}")
