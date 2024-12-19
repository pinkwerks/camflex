import * as common from "./common.js";
import {
    populateCameraDropdown,
    populateLensDropdown,
    setupCameraChangeListener,
    setupSliderAndDistanceListeners
} from "./eventListeners.js";
const inputFeatures = ["sensorWidth", "sensorHeight", "distance"];

// DOM Elements
const cameraSelect = document.getElementById("camera");
const lensSelect = document.getElementById("lens");
const sensorWidthInput = document.getElementById("sensorWidth");
const sensorHeightInput = document.getElementById("sensorHeight");
const slider = document.getElementById("slider");
const distanceInput = document.getElementById("distance");
const outputElement = document.getElementById("output");
const runButton = document.getElementById("runInference");

// Initialize dropdowns and listeners
populateCameraDropdown(cameraSelect);
populateLensDropdown(lensSelect);
setupCameraChangeListener(cameraSelect, sensorWidthInput, sensorHeightInput);
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

        // Get the selected lens
        const lens = lensSelect.value;

        // check if the lens is selected
        if (!lens) {
            throw new Error("Please select a lens.");
        }

        const lens_ = common.formatLensString(lens);
        
        const k1modelpath = `./${lens_}_k1.onnx`;
        const k2modelpath = `./${lens_}_k2.onnx`;
 
        outputElement.textContent += `Loading models:\n${k1modelpath}\n${k2modelpath}\n`;

        // Run inference for K1 and K2
        const [outputData1, outputData2] = await Promise.all([
            common.loadAndRunModel(k1modelpath, values),
            common.loadAndRunModel(k2modelpath, values)
        ]);

        // Display the result
        outputElement.innerHTML += `<div>K1: ${outputData1.toFixed(4)}</div>`;
        outputElement.innerHTML += `<div>K2: ${outputData2.toFixed(4)}</div>`;

    } catch (error) {
        outputElement.innerHTML += `<div style="color: red;">Error: ${error.message || "An unexpected error occurred."}</div>`;
    }
});


