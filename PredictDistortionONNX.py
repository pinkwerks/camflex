import argparse
import numpy as np
import onnxruntime as ort
import os

# Function to query the ONNX model
def run_inference(k1_model_path, k2_model_path, focal_length, k1, k2, sensor_width, sensor_height, distance):
    print("Loading models...")
    k1_session = ort.InferenceSession(k1_model_path)
    k2_session = ort.InferenceSession(k2_model_path)

    # Prepare input data
    input_data = np.array([
        focal_length,  # f0
        k1,      # f1
        k2,      # f2
        sensor_width,  # f3
        sensor_height, # f4
        distance       # f5
    ], dtype=np.float32).reshape(1, -1)  # Batch size = 1, 6 features

    # Prepare ONNX input
    input_name = k1_session.get_inputs()[0].name
    feeds = {input_name: input_data}

    # Run inference
    results = k1_session.run(None, feeds)

    # Process the output
    output_data = results[0]

    print(f"Predicted K1: {output_data}")

    # Prepare input data
    input_data = np.array([
        focal_length,  # f0
        k1,      # f1
        k2,      # f2
        sensor_width,  # f3
        sensor_height, # f4
        distance       # f5
    ], dtype=np.float32).reshape(1, -1)  # Batch size = 1, 6 features

    # Prepare ONNX input
    input_name = k2_session.get_inputs()[0].name
    feeds = {input_name: input_data}

    # Run inference
    results = k2_session.run(None, feeds)

    # Process the output
    output_data = results[0]

    print(f"Predicted K2: {output_data}")

# Main flow to build arguments and run the model
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run inference on a single ONNX model.")
    parser.add_argument("--k1_model", type=str, required=True, help="Path to the K1 model ONNX file.")
    parser.add_argument("--k2_model", type=str, required=True, help="Path to the K2 model ONNX file.")
    parser.add_argument("--focal_length", type=float, required=True, help="Focal length feature.")
    parser.add_argument("--k1", type=float, required=True, help="K1 feature.")
    parser.add_argument("--k2", type=float, required=True, help="K2 feature.")
    parser.add_argument("--sensor_width", type=float, required=True, help="Sensor width feature.")
    parser.add_argument("--sensor_height", type=float, required=True, help="Sensor height feature.")
    parser.add_argument("--distance", type=float, required=True, help="Distance feature.")

    args = parser.parse_args()

    run_inference(
        args.k1_model, args.k2_model,
        args.focal_length, args.k1, args.k2,
        args.sensor_width, args.sensor_height, args.distance
    )