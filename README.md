# Camflex

Use machine learning to predict lens distortion parameters from physical camera characteristics.

You can find the trained ONNX models in the `models` subdirectory.

## Data

The data is housed in private repository - for now. However, a PDF with graphs of the data is availabe in the file `lens_analysis.pdf`

## Trying the models

`python run-onnx.py` 

To predict distortion values K1 and K2 you need to proved a camera's sensor width and sensor height in **CENTIMETERS**. Plus, you must proved the depth in **METERS**

### run-python.py example

`python run-onnx.py -k1 .\models\ARRI-ZEISS_Master_012mm_model_k1.onnx -k2 .\models\ARRI-ZEISS_Master_012mm_model_k2.onnx -W 1.35 -H 1 -d 4`