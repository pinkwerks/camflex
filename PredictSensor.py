import argparse
import numpy as np
import pandas as pd
import joblib
import random
import os

# Set seeds for reproducibility
random.seed(42)
np.random.seed(42)

# Function to build the arguments
def build_args():
    parser = argparse.ArgumentParser(description="Run inference on a model.")
    parser.add_argument('-k1', '--model_k1_path', type=str, required=True, help='Path to the K1 model file')
    parser.add_argument('-k2', '--model_k2_path', type=str, required=True, help='Path to the K2 model file')
    parser.add_argument('-s', '--scaler_path', type=str, required=True, help='Path to the scaler file')
    parser.add_argument('-W', '--sensor_width', type=float, required=True, help='Sensor width parameter value')
    parser.add_argument('-H', '--sensor_height', type=float, required=True, help='Sensor height parameter value')
    parser.add_argument('-d', '--distance', type=float, required=True, help='Distance parameter value')
    return parser.parse_args()

# Function to query the models
def query_models(args):
    try:
        # Load the StandardScaler
        if not os.path.exists(args.scaler_path):
            raise FileNotFoundError(f"Scaler file not found: {args.scaler_path}")
        scaler = joblib.load(args.scaler_path)

        # Load the models
        if not os.path.exists(args.model_k1_path):
            raise FileNotFoundError(f"K1 model file not found: {args.model_k1_path}")
        model_k1 = joblib.load(args.model_k1_path)

        if not os.path.exists(args.model_k2_path):
            raise FileNotFoundError(f"K2 model file not found: {args.model_k2_path}")
        model_k2 = joblib.load(args.model_k2_path)

        # Create input DataFrame with feature names
        input_data = pd.DataFrame([[args.sensor_width, args.sensor_height, args.distance]], 
                                  columns=['SensorW', 'SensorH', 'Distance'], dtype=np.float32)

        # Scale input data
        scaled_input_data = scaler.transform(input_data).astype(np.float32)

        # Run inference
        k1_pred = model_k1.predict(scaled_input_data)
        k2_pred = model_k2.predict(scaled_input_data)

        # Print result
        print(f'{k1_pred[0]}, {k2_pred[0]}')

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred (Are you loading .pk1 files and the correct scaler?): {e}")

# Main flow to build arguments and run the models
if __name__ == '__main__':
    args = build_args()
    query_models(args)
