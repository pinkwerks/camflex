import os
import json
import csv
import sys
import argparse

# Function to convert JSON to CSV
def convert_json_to_csv(json_file_path, output_dir):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Extract necessary data
    lens_params = data["AutodeskFlame3DELensDistortion"]["LensParams"]
    focal_length = data["AutodeskFlame3DELensDistortion"]["FocalLength"][0] * 10  # Convert cm to mm
    focus_distances = data["AutodeskFlame3DELensDistortion"]["FocusDistance"]
    model_params = data["AutodeskFlame3DELensDistortion"]["ModelParams"]
    sensor_aspect = lens_params.get("FilmAspect", None)

    # Filter out distances greater than 500000
    filtered_distances = [d for d in focus_distances if d <= 500000]

    # Prepare data for CSV
    csv_data = []

    for i, distance in enumerate(filtered_distances):
        row = {
            "Distance": distance,
            "FocalLength": focal_length,
            "K1": model_params["Distortion - Degree 2"][i] if i < len(model_params["Distortion - Degree 2"]) else None,
            "K2": model_params["U - Degree 2"][i] if i < len(model_params["U - Degree 2"]) else None,
            "K3": model_params["V - Degree 2"][i] if i < len(model_params["V - Degree 2"]) else None,
            "P1": model_params["U - Degree 4"][i] if i < len(model_params["U - Degree 4"]) else None,
            "P2": model_params["V - Degree 4"][i] if i < len(model_params["V - Degree 4"]) else None,
            "SensorAspect": sensor_aspect
        }
        csv_data.append(row)

    # Write to CSV
    csv_file_name = os.path.splitext(os.path.basename(json_file_path))[0] + '.csv'
    csv_file_path = os.path.join(output_dir, csv_file_name)
    csv_headers = ["Distance", "FocalLength", "K1", "K2", "K3", "P1", "P2", "SensorAspect"]

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"Data successfully written to {csv_file_path}")

# Main function to process all JSON files in a directory
def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            json_file_path = os.path.join(input_dir, file_name)
            convert_json_to_csv(json_file_path, output_dir)

# Entry point for the script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JSON files to CSV.")
    parser.add_argument("input_directory", help="Path to the directory containing JSON files.")
    parser.add_argument("output_directory", help="Path to the directory where CSV files will be saved.")

    args = parser.parse_args()

    process_directory(args.input_directory, args.output_directory)
