import os
import json
import csv
import sys
import argparse

# Function to convert JSON to CSV
def convert_json_to_csv(json_file_path, output_dir, focal_length_override=None, convert_from_inches_to_mm=False):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Extract necessary data
    lens_params = data["AutodeskFlame3DELensDistortion"]["LensParams"]
    focal_length = focal_length_override if focal_length_override is not None else data["AutodeskFlame3DELensDistortion"]["FocalLength"][0]
    focus_distances = data["AutodeskFlame3DELensDistortion"]["FocusDistance"]
    model_params = data["AutodeskFlame3DELensDistortion"]["ModelParams"]

    # Convert sensor dimensions to mm if the flag is provided
    sensor_width = lens_params["FBackWidth"]
    sensor_height = lens_params["FBackHeight"]

    if convert_from_inches_to_mm:
        sensor_width *= 25.4  # Convert inches to mm
        sensor_height *= 25.4  # Convert inches to mm

    # Prepare data for CSV
    csv_data = []

    for i, distance in enumerate(focus_distances):
        row = {
            "Distance": distance,
            "focalLength": focal_length,
            "K1": model_params["Distortion - Degree 2"][i] if i < len(model_params["Distortion - Degree 2"]) else None,
            "K2": model_params["U - Degree 2"][i] if i < len(model_params["U - Degree 2"]) else None,
            "K3": model_params["V - Degree 2"][i] if i < len(model_params["V - Degree 2"]) else None,
            "P1": model_params["U - Degree 4"][i] if i < len(model_params["U - Degree 4"]) else None,
            "P2": model_params["V - Degree 4"][i] if i < len(model_params["V - Degree 4"]) else None,
            "SensorH": sensor_height,
            "SensorW": sensor_width,
            "FrameH": sensor_height,  # Assuming FrameH is the same as SensorH
            "FrameW": sensor_width,   # Assuming FrameW is the same as SensorW
        }
        csv_data.append(row)

    # Write to CSV
    csv_file_name = os.path.splitext(os.path.basename(json_file_path))[0] + '.csv'
    csv_file_path = os.path.join(output_dir, csv_file_name)
    csv_headers = ["Distance", "focalLength", "K1", "K2", "K3", "P1", "P2", "SensorH", "SensorW", "FrameH", "FrameW"]

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"Data successfully written to {csv_file_path}")

# Main function to process all JSON files in a directory
def process_directory(input_dir, output_dir, focal_length_override, convert_from_inches_to_mm):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            json_file_path = os.path.join(input_dir, file_name)
            convert_json_to_csv(json_file_path, output_dir, focal_length_override, convert_from_inches_to_mm)

# Entry point for the script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JSON files to CSV.")
    parser.add_argument("input_directory", help="Path to the directory containing JSON files.")
    parser.add_argument("output_directory", help="Path to the directory where CSV files will be saved.")
    parser.add_argument("--focal_length", type=float, help="Optional focal length value to override the JSON value.")
    parser.add_argument("--convert_from_inches_to_mm", action="store_true", help="Flag to convert sensor dimensions from inches to millimeters.")

    args = parser.parse_args()

    process_directory(args.input_directory, args.output_directory, args.focal_length, args.convert_from_inches_to_mm)
