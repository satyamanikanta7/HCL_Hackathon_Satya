from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TransactionUploadResponse(BaseModel):
    total_transactions: int
    flagged_count: int
    flagged: List[dict]
    message: Optional[str] = None

class FlaggedTransactionResponse(BaseModel):
    flagged_transactions: List[dict]

class NotificationResponse(BaseModel):
    status: str
    count: int
    message: Optional[str] = None

class DashboardStats(BaseModel):
    total_transactions: int
    flagged_transactions: int
    fraud_rate: float
    last_scan_time: Optional[datetime] = None
    high_risk_transactions: int
    medium_risk_transactions: int
    low_risk_transactions: int

class AuditLog(BaseModel):
    id: int
    action: str
    timestamp: datetime
    user: str
    details: str
    status: str
