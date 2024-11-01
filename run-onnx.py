import onnxruntime as ort
import numpy as np
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Run inference on an ONNX model for camera distortion parameters.")
parser.add_argument('--model', type=str, required=True, help="Path to the ONNX model file.")
parser.add_argument('--focal_length', type=float, required=True, help="Focal length value.")
parser.add_argument('--sensor_aspect', type=float, required=True, help="Sensor aspect ratio value.")
parser.add_argument('--distance', type=float, required=True, help="Distance value.")

# Parse the arguments
args = parser.parse_args()

# Load the ONNX model
session = ort.InferenceSession(args.model)

# Prepare the input data
input_data = np.array([[args.focal_length, args.sensor_aspect, args.distance]], dtype=np.float32)

# Get the input name for the ONNX model
input_name = session.get_inputs()[0].name

# Run inference
outputs = session.run(None, {input_name: input_data})

# Print the outputs
print(f"Predicted Distortion Parameters (K1, K2, K3) for focal length {args.focal_length}, sensor aspect ratio {args.sensor_aspect}, and distance {args.distance}: {outputs}")
