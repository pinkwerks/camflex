import onnx
import argparse

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Analyze an ONNX model's inputs and outputs.")
    parser.add_argument("model_path", type=str, help="Path to the ONNX model file.")
    args = parser.parse_args()

    # Load the ONNX model
    model = onnx.load(args.model_path)

    # Get model graph information
    graph = model.graph

    # List inputs
    print("Inputs:")
    for input_tensor in graph.input:
        print(f"Name: {input_tensor.name}")
        for dim in input_tensor.type.tensor_type.shape.dim:
            print(f"  - Dimension: {dim.dim_value}")

    # List outputs
    print("\nOutputs:")
    for output_tensor in graph.output:
        print(f"Name: {output_tensor.name}")
        for dim in output_tensor.type.tensor_type.shape.dim:
            print(f"  - Dimension: {dim.dim_value}")

    # Look for feature names (often stored as metadata)
    metadata = model.metadata_props
    print("\nMetadata Properties:")
    for prop in metadata:
        print(f"{prop.key}: {prop.value}")

if __name__ == "__main__":
    main()
