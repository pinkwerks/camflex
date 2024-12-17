import argparse
import numpy as np
import onnxruntime as ort

# Function to query the combined ONNX model
def run_inference(k1_model_path, k2_model_path, k1, k2, sensor_width, sensor_height, distance):
    print("Loading model...")
    k1_session = ort.InferenceSession(k1_model_path)
    k2_session = ort.InferenceSession(k2_model_path)

    # Prepare raw input data
    raw_input_data = np.array([
        k1,           # f0
        k2,           # f1
        sensor_width, # f2
        sensor_height,# f3
        distance      # f4
    ], dtype=np.float32).reshape(1, -1)  # Batch size = 1, 5 features

    # Run K1 model (scaling + prediction integrated)
    k1_input_name = k1_session.get_inputs()[0].name
    k1_feeds = {k1_input_name: raw_input_data}
    k1_results = k1_session.run(None, k1_feeds)[0]

    # Run K2 model (scaling + prediction integrated)
    k2_input_name = k2_session.get_inputs()[0].name
    k2_feeds = {k2_input_name: raw_input_data}
    k2_results = k2_session.run(None, k2_feeds)[0]

    print(f"Predicted K1: {k1_results[0][0]}")
    print(f"Predicted K2: {k2_results[0][0]}")

# Main flow to build arguments and run the model
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run inference on a ONNX model.")
    parser.add_argument("-k1m", "--k1_model", type=str, required=True, help="Path to the K1 ONNX file.")
    parser.add_argument("-k2m", "--k2_model", type=str, required=True, help="Path to the K2 ONNX file.")
    parser.add_argument("-k1", "--k1", type=float, required=True, help="K1 feature.")
    parser.add_argument("-k2", "--k2", type=float, required=True, help="K2 feature.")
    parser.add_argument("-sw", "--sensor_width", type=float, required=True, help="Sensor width feature. (centimeters)")
    parser.add_argument("-sh", "--sensor_height", type=float, required=True, help="Sensor height feature. (centimeters)")
    parser.add_argument("-d", "--distance", type=float, required=True, help="Distance feature. (centimeters)")

    args = parser.parse_args()

    run_inference(
        args.k1_model,
        args.k2_model,
        args.k1,
        args.k2,
        args.sensor_width, 
        args.sensor_height, 
        args.distance
    )
