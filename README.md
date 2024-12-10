# Camflex
Use machine learning to predict [lens distortion](https://en.wikipedia.org/wiki/Distortion_(optics)) parameters for lenses used in motion picture photography.

## Lenses sampled
- ARRI / ZEISS Master
- Arriflex / ZEISS
- ZEISS CP2
- ZEISS CP3
- ZEISS Supreme

## Cameras sampled
- Alexa 35
- Alexa 65
- Alexa LF
- Alexa Mini
- Alexa SXT
- PANAVISION DXL
- RED Dragon
- RED Mysterium X
- RED Weapon S35
- SONY F55
- SONY F65
- SONY Venice 2

## Requirements
To train or run inference on the ONNX models from the command line you'll need [Python 3](https://www.python.org/downloads/) and some libraries.

`python3 -m pip install -r requirements.txt`

## Try out the models from the command line
You can find the trained ONNX models in the `models` subdirectory. Run this to get help.

`python3 run-onnx.py`

To predict distortion values *K1* and *K2* you need to provide a camera's sensor-width and sensor-height in **CENTIMETERS**. Plus, you must provide the depth in **METERS**.

### run-onnx.py example
`python3 run-onnx.py -k1 .\models\ARRI-ZEISS_Master_012mm_model_k1.onnx -k2 .\models\ARRI-ZEISS_Master_012mm_model_k2.onnx -W 1.35 -H 1 -d 4`

## Data
The data is housed in a [private repository](https://github.com/pinkwerks/camflex-data) for now. However, a PDF with graphs of the data is available in the file `lens_analysis.pdf`.

Special thanks to [Andy Davis](https://imag4media.com/) for collecting, organizing, and supplying the initial data that inspired me to try this.

### Working with the data submodule (assuming you have permission)
After cloning this repo you can get the camflex-data submodule like this:

`git submodule update --init --recursive`

Get status:

`git submodule status`

And update it like this:

`git submodule update --remote`