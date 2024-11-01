import pandas as pd
import os
import sys

# Get the input and output directory paths from command line arguments
def main(input_directory, output_directory):
    if not os.path.isdir(input_directory):
        print(f"Error: Provided input path '{input_directory}' is not a directory.")
        sys.exit(1)

    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    # Iterate over all CSV files in the provided input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_directory, filename)
            df = pd.read_csv(file_path)

            # Compute the new column 'SensorAspect' by dividing 'SensorW' by 'SensorH'
            df['SensorAspect'] = df['SensorW'] / df['SensorH']

            # Remove 'FrameW', 'FrameH', 'SensorW', and 'SensorH' columns
            df = df.drop(columns=['FrameW', 'FrameH', 'SensorW', 'SensorH'])

            # Rename 'focalLength' to 'FocalLength'
            df = df.rename(columns={'focalLength': 'FocalLength'})

            # Drop rows where 'K1', 'K2', 'P1', and 'P2'
            zero_columns = ['K1', 'K2', 'P1', 'P2']
            df = df[~((df[zero_columns] == 0).all(axis=1))]

            # Save the modified DataFrame to a new CSV file in the output directory
            filename_without_ext, ext = os.path.splitext(filename)
            output_file_path = os.path.join(output_directory, f"{filename_without_ext}_modified{ext}")
            df.to_csv(output_file_path, index=False)

            print(f"Modified CSV saved to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_directory> <output_directory>")
        sys.exit(1)
    
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    main(input_directory, output_directory)