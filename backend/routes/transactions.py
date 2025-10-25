from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import pandas as pd
import io
from backend.services.auditor_service import AuditorDashboardService
from backend.schemas.fraud import TransactionUploadResponse, FlaggedTransactionResponse, NotificationResponse
from backend.routes.deps import get_current_user
from backend.models.user import User

router = APIRouter()
auditor_service = AuditorDashboardService()

@router.post("/upload-csv", response_model=TransactionUploadResponse)
def upload_csv(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    """
    Upload CSV file, run fraud detection, and return comprehensive results.
    Requires authentication.
    """
    try:
        # Read CSV file
        df = pd.read_csv(file.file)
        
        # Process transactions using auditor service
        result = auditor_service.process_transactions(df, current_user.email)
        
        return TransactionUploadResponse(
            total_transactions=result["total_transactions"],
            flagged_count=result["flagged_count"],
            flagged=result["flagged"],
            message=f"Processed {result['total_transactions']} transactions, {result['flagged_count']} flagged as suspicious"
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

@router.get("/flagged", response_model=FlaggedTransactionResponse)
def get_flagged(current_user: User = Depends(get_current_user)):
    """
    View flagged suspicious transactions from the last upload.
    Requires authentication.
    """
    try:
        result = auditor_service.get_flagged_transactions()
        return FlaggedTransactionResponse(flagged_transactions=result["flagged_transactions"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving flagged transactions: {str(e)}")

@router.post("/notify-admin", response_model=NotificationResponse)
def notify_admin(current_user: User = Depends(get_current_user)):
    """
    Send an email to admin with list of flagged suspicious transactions.
    Requires authentication.
    """
    try:
        result = auditor_service.send_notification()
        return NotificationResponse(
            status=result["status"],
            count=result["count"],
            message=result["message"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending notification: {str(e)}")

