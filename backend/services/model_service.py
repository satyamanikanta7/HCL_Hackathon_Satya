import joblib
import pandas as pd
from backend.core.config import settings

model = None
scaler = None

def load_model():
    """Load the trained model and scaler from files."""
    global model, scaler
    try:
        model = joblib.load(settings.MODEL_PATH)
        scaler = joblib.load(settings.SCALER_PATH)
        print("Model and scaler loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise ValueError("Model or scaler not found. Please train the model first.")

def predict(df: pd.DataFrame) -> pd.DataFrame:
    """Run fraud detection on uploaded DataFrame with optional metadata columns."""
    global model, scaler
    
    if model is None or scaler is None:
        load_model()
    
    if model is None or scaler is None:
        raise ValueError("Model or scaler not loaded. Please train first.")

    # Preserve metadata columns
    meta_cols = [col for col in ["Name", "ID", "Time"] if col in df.columns]

    # Get numeric columns only
    df_numeric = df.select_dtypes(include=["number"])

    # Ensure we have the expected columns for the scaler
    if hasattr(scaler, "feature_names_in_"):
        expected_cols = list(scaler.feature_names_in_)
        common_cols = [col for col in expected_cols if col in df_numeric.columns]
        df_numeric = df_numeric[common_cols]
    else:
        df_numeric = df_numeric

    # Scale the data
    X_scaled = scaler.transform(df_numeric)

    # Get predictions and scores
    scores = model.decision_function(X_scaled)
    preds = model.predict(X_scaled)

    # Add results to dataframe
    df["fraud_score"] = scores
    df["predicted_label"] = preds
    df["flagged"] = (preds == -1)

    # Sort by fraud score (most suspicious first)
    df = df.sort_values("fraud_score")

    # Return relevant columns
    return df[meta_cols + ["fraud_score", "flagged"] + list(df_numeric.columns)]
