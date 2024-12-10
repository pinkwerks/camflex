import argparse
import onnxruntime as ort
import numpy as np
import pandas as pd
import random
import os

# Set seeds for reproducibility
random.seed(42)
np.random.seed(42)
ort.set_seed(42)

# Function to build the arguments
def build_args():
    parser = argparse.ArgumentParser(description="Run inference on ONNX models for K1 and K2.")
    parser.add_argument('-k1', '--k1_model_path', type=str, required=True, help='Path to the ONNX model for K1')
    parser.add_argument('-k2', '--k2_model_path', type=str, required=True, help='Path to the ONNX model for K2')
    parser.add_argument('-W', '--sensor_width', type=float, required=True, help='Sensor width parameter value')
    parser.add_argument('-H', '--sensor_height', type=float, required=True, help='Sensor height parameter value')
    parser.add_argument('-d', '--distance', type=float, required=True, help='Distance parameter value')
    parser.add_argument('--device', type=str, default='cpu', choices=['cpu', 'cuda'], help='Device to run the models on')
    return parser.parse_args()

# Function to query the models
def query_models(args):
    try:
        # Load ONNX model sessions
        for model_path in [args.k1_model_path, args.k2_model_path]:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")

        providers = ['CUDAExecutionProvider'] if args.device == 'cuda' else ['CPUExecutionProvider']

        # Load sessions for K1 and K2
        k1_session = ort.InferenceSession(args.k1_model_path, providers=providers)
        k2_session = ort.InferenceSession(args.k2_model_path, providers=providers)

        # Create input DataFrame with feature names
        input_data = pd.DataFrame([[args.sensor_width, args.sensor_height, args.distance]], 
                                  columns=['SensorW', 'SensorH', 'Distance'], dtype=np.float32)

        # Run inference for K1
        k1_inputs = {k1_session.get_inputs()[0].name: input_data.values.astype(np.float32)}
        k1_outs = k1_session.run(None, k1_inputs)
        k1_prediction = k1_outs[0][0]

        # Run inference for K2
        k2_inputs = {k2_session.get_inputs()[0].name: input_data.values.astype(np.float32)}
        k2_outs = k2_session.run(None, k2_inputs)
        k2_prediction = k2_outs[0][0]

        # Print results
        print(f'Predicted value for K1: {k1_prediction}')
        print(f'Predicted value for K2: {k2_prediction}')

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Main flow to build arguments and run the models
if __name__ == '__main__':
    args = build_args()
    query_models(args)
