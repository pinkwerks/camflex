import * as common from "./common.js";
import {
    populateCameraDropdown,
    populateLensDropdown,
    setupCameraChangeListener,
    setupLensChangeListener,
    setupSliderAndDistanceListeners
} from "./eventListeners.js";
const inputFeatures = ["k1", "k2", "sensorWidth", "sensorHeight", "distance"];

// DOM Elements
const k1 = document.getElementById("k1");
const k2 = document.getElementById("k2");
const cameraSelect = document.getElementById("camera");
const lensSelect = document.getElementById("lens");
const sensorWidthInput = document.getElementById("sensorWidth");
const sensorHeightInput = document.getElementById("sensorHeight");
const focalLengthInput = document.getElementById("focalLength");
const slider = document.getElementById("slider");
const distanceInput = document.getElementById("distance");
const outputElement = document.getElementById("output");
const runButton = document.getElementById("runInference");

// Initialize dropdowns and listeners
populateCameraDropdown(cameraSelect);
populateLensDropdown(lensSelect);
setupCameraChangeListener(cameraSelect, sensorWidthInput, sensorHeightInput);
setupLensChangeListener(lensSelect, focalLengthInput);
setupSliderAndDistanceListeners(slider, distanceInput);

// Run inference on button click
runButton.addEventListener("click", async () => {
    // Clear the output element
    outputElement.textContent = ""; // Clear previous output

    try {
        // Validate and prepare input data
        const values = inputFeatures.map(id => {
            const result = common.parseAndValidateNumber(id, "float", 0);
            if (!result.valid) throw new Error(result.error || `Invalid value for ${id}.`);
            return result.value;
        });

        // Retrieve and validate focal length
        const focalLengthResult = common.parseAndValidateNumber("focalLength", "int", 1);
        if (!focalLengthResult.valid) throw new Error(focalLengthResult.error || "Invalid focal length.");
        const focalLength = focalLengthResult.value;

        // Validate lens availability
        const focalLengthValidation = common.validateFocalLength(focalLength);
        if (!focalLengthValidation.valid) throw new Error(focalLengthValidation.error);

        const k1modelpath = `models/${focalLength}mm_c_k1.onnx`;
        const k2modelpath = `models/${focalLength}mm_c_k2.onnx`;

        outputElement.textContent += `Loading models:\n${k1modelpath}\n${k2modelpath}\n`;

        // Run inference for K1 and K2
        const [outputData1, outputData2] = await Promise.all([
            common.loadAndRunModel(k1modelpath, values),
            common.loadAndRunModel(k2modelpath, values)
        ]);

        // Display the result
        outputElement.innerHTML += `<div>K1: ${outputData1.toFixed(4)}</div>`;
        outputElement.innerHTML += `<div>K2: ${outputData2.toFixed(4)}</div>`;

        // Get the model image and display it
        const modeimgpath = `models/${focalLength}mm_c.png`;
        const img = document.createElement("img");
        img.src = modeimgpath;
        img.style.width = "100%";
        outputElement.appendChild(img);
    } catch (error) {
        outputElement.innerHTML += `<div style="color: red;">Error: ${error.message || "An unexpected error occurred."}</div>`;
    }
});


