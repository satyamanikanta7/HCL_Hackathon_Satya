import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score

def load_data(path: str = "creditcard.csv"):
    df = pd.read_csv(path)
    print(f"Data loaded: {df.shape}")
    return df

def preprocess(df: pd.DataFrame):
    # Drop nulls if any
    df = df.dropna()

    # Separate target if available
    if "Class" in df.columns:
        y = df["Class"]
        X = df.drop("Class", axis=1)
    else:
        y = None
        X = df.copy()

    # Drop non-numeric columns
    for col in X.columns:
        if pd.api.types.is_datetime64_any_dtype(X[col]) or X[col].dtype == object:
            print(f"Dropping non-numeric column: {col}")
            X = X.drop(columns=[col])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y, scaler

def train_isolation_forest(X_scaled: np.ndarray, y: np.ndarray = None):
    print("Training Isolation Forest...")
    outlier_fraction = None
    if y is not None:
        n_fraud = len(y[y == 1])
        n_valid = len(y[y == 0])
        outlier_fraction = n_fraud / float(n_valid)
        print(f"Outlier fraction: {outlier_fraction:.5f}")
    contamination = outlier_fraction if outlier_fraction else 0.01

    model = IsolationForest(
        n_estimators=100,
        max_samples=len(X_scaled),
        contamination=contamination,
        random_state=42,
        verbose=0
    )
    model.fit(X_scaled)
    return model

def evaluate_model(model, X_scaled, y):
    y_pred = model.predict(X_scaled)
    y_pred[y_pred == 1] = 0 
    y_pred[y_pred == -1] = 1

    if y is not None:
        print("Accuracy:", accuracy_score(y, y_pred))
        print("Classification Report:")
        print(classification_report(y, y_pred))

def main():
    DATA_PATH = "ml_model\data\creditcard.csv"
    MODEL_PATH = "ml_model/model.joblib"
    SCALER_PATH = "ml_model/scaler.joblib"

    df = load_data(DATA_PATH)
    X_scaled, y, scaler = preprocess(df)
    model = train_isolation_forest(X_scaled, y)
    evaluate_model(model, X_scaled, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print(f"Scaler saved to {SCALER_PATH}")

if __name__ == "__main__":
    main()
