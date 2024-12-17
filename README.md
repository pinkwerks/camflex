# Camflex
Use machine learning to predict [lens distortion](https://en.wikipedia.org/wiki/Distortion_(optics)) parameters for lenses used in motion picture photography.

## Try it here!

[Camflex](https://pinkwerks.github.io/camflex)

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
- Panavision DXL
- Panavision DXL
- RED Dragon
- RED Mysterium X
- RED Weapon S35
- SONY F55
- SONY F65
- SONY Venice 2

## Quality
I'm no data scientist. Graphs of the predictions can be found near the bottom of the [notebook](Camflex.ipynb). Some are better than others. I was inspired to help out VFX artists who had plates and camera data - but no grids. Typically, you'd film the distortion grids and run them through something like [3DE](https://www.3dequalizer.com/) to get the highest quality results.

## Get the requirements
To train or run inference on the ONNX models from the command line, you'll need [Python 3](https://www.python.org/downloads/) and some libraries.

`python3 -m pip install -r requirements.txt`

## Try out the models from the command line
You can find the trained ONNX models in the [`models`](models) subdirectory. There are 2 main categories: *focal length models* and *lens models*. There are separate models for each feature (K1, K2) for prediction. You always make predictions for a focus in distance centimeters.

**Lens models** make predictions for a specific lens. These are models named by manufacturer at specific focal length. An "ARRI / ZEISS Master 50mm", for example.

**Focal length models** let you predict distortion for a family of lens models, if you have the camera sensor sizes.

Run `python3 ConvertDistortionONNX.py -h` or `python3 PredictDistortion.py -h` for help.

### Use a ***focal length model*** to retarget K1 and K2 (using exising distortion to a new camera 1m away)
If you already have **K1** and **K2**, you can convert those values using a **focal length model** (`50mm_k1.onnx` for example) a distance and the target sensor size. This is like swapping camera bodies when you already have a lens and it's distortion values.
```
python3 ConvertDistortionONNX.py \
    -k1m .\models\50mm_k1.onnx \
    -k2m .\models\50mm_k2.onnx \
    -k1 0.014903 \
    -k2 -0.000562 \
    -sw 2.799 \
    -sh 1.9218828124999998 \
    -d 100
```

### Use a ***lens model*** to predict K1 and K2 (for a specific lens, 1m away)
If you know the physical characteristics of your camera and you want distortion values for a specific lens (like the ARRI-ZEISS_Master_050mm) you can apply a **lens model**.

```
python3 PredictDistortionONNX.py \
    -k1m .\models\ARRI-ZEISS_Master_050mm_k1.onnx \
    -k2m .\models\ARRI-ZEISS_Master_050mm_k2.onnx \
    -sw 2.799 \
    -sh 1.92 \
    -d 100
```
## Try out in web browser
Ensure [node.js](https://nodejs.org/en/download/prebuilt-installer) is installed.
```
cd public
npx http-server
```
Then visit url printed in console.

## Data
The data is housed in a [private repository](https://github.com/pinkwerks/camflex-data) for now. However, a PDF with graphs of the data is available in the file [lens_data.pdf](lens_data.pdf).

Special thanks to [Andy Davis](https://imag4media.com/) for collecting, organizing, and supplying the initial data that inspired me to try this.

### Working with the data submodule (assuming you have permission)
After cloning this repo, you can get the camflex-data submodule like this:

`git submodule update --init --recursive`

Get status:

`git submodule status`

And update it like this:

`git submodule update --remote`