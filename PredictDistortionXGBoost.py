import xgboost as xgb
import joblib
import numpy as np
import argparse

def run_inference(model_path, scaler, focal_length, k1, k2, sensor_width, sensor_height, distance):
    # Load the models and scaler
    print("Loading models and scaler...")
    k1_model = xgb.Booster()
    k1_model.load_model(model_path)

    scaler = joblib.load(scaler)

    # Prepare the input features
    features = np.array([[focal_length, k1, k2, sensor_width, sensor_height, distance]])
    feature_names = ["f0", "f1", "f2", "f3", "f4", "f5"]
    
    if features.shape[1] != scaler.mean_.shape[0]:
        raise ValueError(
            f"Feature length mismatch. Expected {scaler.mean_.shape[0]}, got {features.shape[1]}."
        )

    # Scale the input features
    print("Scaling features...")
    features_scaled = scaler.transform(features)

    # Convert scaled features to DMatrix for XGBoost inference
    features_dmatrix = xgb.DMatrix(features_scaled, feature_names=feature_names)

    # Run predictions
    print("Running predictions...")
    prediction = k1_model.predict(features_dmatrix)

    print(f"Predicted: {prediction[0]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run inference using XGBoost JSON models and scaler.")
    parser.add_argument("--model", type=str, required=True, help="Path to the K1 model JSON file.")
    parser.add_argument("--scaler", type=str, required=True, help="Path to the K1 scaler joblib file.")
    parser.add_argument("--focal_length", type=float, required=True, help="Focal length feature.")
    parser.add_argument("--k1", type=float, required=True, help="K1 feature.")
    parser.add_argument("--k2", type=float, required=True, help="K2 feature.")
    parser.add_argument("--sensor_width", type=float, required=True, help="Sensor width feature.")
    parser.add_argument("--sensor_height", type=float, required=True, help="Sensor height feature.")
    parser.add_argument("--distance", type=float, required=True, help="Distance feature.")

    args = parser.parse_args()

    prediction = run_inference(
        args.model, args.k2_model,
        args.scaler, args.k2_scaler,
        args.focal_length, args.k1, args.k2,
        args.sensor_width,args.sensor_height, args.distance
    )
