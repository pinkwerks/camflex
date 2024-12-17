import xgboost as xgb
import joblib
import numpy as np
import argparse

def run_inference(k1m, k2m, k1s, k2s, sensor_width, sensor_height, distance):
    # Load the models and scaler
    print("Loading models and scaler...")
    k1_model = xgb.Booster()
    k1_model.load_model(k1m)
    k2_model = xgb.Booster()
    k2_model.load_model(k2m)

    k1_scaler = joblib.load(k1s)
    k2_scaler = joblib.load(k2s)

    # Prepare the input features
    features = np.array([[sensor_width, sensor_height, distance]])
    feature_names = ["f0", "f1", "f2"]
    
    if features.shape[1] != k1_scaler.mean_.shape[0]:
        raise ValueError(
            f"Feature length mismatch. Expected {k1_scaler.mean_.shape[0]}, got {features.shape[1]}."
        )
    
    if features.shape[1] != k2_scaler.mean_.shape[0]:
        raise ValueError(
            f"Feature length mismatch. Expected {k2_scaler.mean_.shape[0]}, got {features.shape[1]}."
        )


    # Scale the input features
    print("Scaling features...")
    features_scaled = k1_scaler.transform(features)
    features_scaled2 = k2_scaler.transform(features)

    # Convert scaled features to DMatrix for XGBoost inference
    features_dmatrix = xgb.DMatrix(features_scaled, feature_names=feature_names)
    features_dmatrix2 = xgb.DMatrix(features_scaled2, feature_names=feature_names)

    # Run predictions
    print("Running predictions...")
    prediction = k1_model.predict(features_dmatrix)
    prediction2 = k2_model.predict(features_dmatrix2)

    print(f"K1: {prediction[0]}")
    print(f"K2: {prediction2[0]}")

# Main flow to build arguments and run the model
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run inference on a ONNX model.")
    parser.add_argument("-k1m", "--k1_model", type=str, required=True, help="Path to the K1 JSON file.")
    parser.add_argument("-k2m", "--k2_model", type=str, required=True, help="Path to the K2 JSON file.")
    parser.add_argument("-k1s", "--k1_scaler", type=str, required=True, help="Path to the K1 scaler.")
    parser.add_argument("-k2s", "--k2_scaler", type=str, required=True, help="Path to the K2 scaler.")
    parser.add_argument("-sw", "--sensor_width", type=float, required=True, help="Sensor width feature. (centimeters)")
    parser.add_argument("-sh", "--sensor_height", type=float, required=True, help="Sensor height feature. (centimeters)")
    parser.add_argument("-d", "--distance", type=float, required=True, help="Distance feature. (centimeters)")

    args = parser.parse_args()

    run_inference(
        args.k1_model,
        args.k2_model,
        args.k1_scaler,
        args.k2_scaler,
        args.sensor_width, 
        args.sensor_height, 
        args.distance
    )
