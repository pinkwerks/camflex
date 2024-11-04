import os
import json
import csv
import sys
import argparse

# Function to convert JSON to CSV
def convert_json_to_csv(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Extract necessary data
    lens_params = data["AutodeskFlame3DELensDistortion"]["LensParams"]
    focus_distances = data["AutodeskFlame3DELensDistortion"]["FocusDistance"]
    model_params = data["AutodeskFlame3DELensDistortion"]["ModelParams"]
    
    sensor_width = lens_params.get("FBackWidth", None)
    sensor_height = lens_params.get("FBackHeight", None)

    # Filter out distances greater than 500000
    filtered_distances = [d for d in focus_distances if d <= 500000]

    # Prepare data for CSV
    csv_data = []

    for i, distance in enumerate(filtered_distances):
        row = {
            "Distance": distance,
            "K1": model_params["Distortion - Degree 2"][i] if i < len(model_params["Distortion - Degree 2"]) else None,
            "K2": model_params["U - Degree 2"][i] if i < len(model_params["U - Degree 2"]) else None,
            "SensorW": sensor_width,
            "SensorH": sensor_height
        }
        csv_data.append(row)

    # Remove the last row
    if csv_data:
        csv_data.pop()

    # Write to CSV
    csv_file_name = os.path.splitext(os.path.basename(json_file_path))[0] + '.csv'
    csv_file_path = os.path.join(os.path.dirname(json_file_path), csv_file_name)
    csv_headers = ["Distance", "K1", "K2", "SensorW", "SensorH"]

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"Data successfully written to {csv_file_path}")

# Main function to process all JSON files in a directory
def process_directory(input_dir):
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            json_file_path = os.path.join(input_dir, file_name)
            convert_json_to_csv(json_file_path)

# Entry point for the script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JSON files to CSV.")
    parser.add_argument("input_directory", help="Path to the directory containing JSON files.")

    args = parser.parse_args()

    process_directory(args.input_directory)