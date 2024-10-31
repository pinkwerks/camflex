import pandas as pd
import os
import sys

# Get the directory path from command line arguments
def main(directory_path):
    if not os.path.isdir(directory_path):
        print(f"Error: Provided path '{directory_path}' is not a directory.")
        sys.exit(1)

    # Iterate over all CSV files in the provided directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(file_path)

            # Compute the new column 'SensorAspect' by dividing 'SensorW' by 'SensorH'
            df['SensorAspect'] = df['SensorW'] / df['SensorH']

            # Remove 'FrameW', 'FrameH', 'SensorW', and 'SensorH' columns
            df = df.drop(columns=['FrameW', 'FrameH', 'SensorW', 'SensorH'])

            # Rename 'focalLength' to 'FocalLength'
            df = df.rename(columns={'focalLength': 'FocalLength'})
            # Save the modified DataFrame to a new CSV file
            filename_without_ext, ext = os.path.splitext(filename)
            output_file_path = os.path.join(directory_path, f"{filename_without_ext}_modified{ext}")
            df.to_csv(output_file_path, index=False)

            print(f"Modified CSV saved to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    main(directory_path)
