const cameraData = {
    "Alexa 35 3k": { sensorW: 2.021926, sensorH: 1.695064 },
    "Alexa 35 HD": { sensorW: 2.488889, sensorH: 1.4 },
    "Alexa 35 (open gate)": { sensorW: 2.799084, sensorH: 1.921941 },
    "Alexa 65 (open gate)": { sensorW: 5.413059, sensorH: 2.558 },
    "Alexa LF HD": { sensorW: 3.168, sensorH: 1.782 },
    "Alexa LF (open gate)": { sensorW: 3.669656, sensorH: 2.554239 },
    "Alexa Mini (open gate)": { sensorW: 2.825342, sensorH: 1.816999 },
    "Alexa SXT 2.8k": { sensorW: 2.376, sensorH: 1.782 },
    "PANAVISION DXL2 (full-frame)": { sensorW: 2.048, sensorH: 1.08 },
    "PANAVISION DXL2 HD": { sensorW: 2.88, sensorH: 1.62 },
    "PANAVISION DXL2 (open gate)": { sensorW: 4.232533, sensorH: 2.232 },
    "PANAVISION DXL HD": { sensorW: 3.072, sensorH: 1.728 },
    "RED_Dragon HD": { sensorW: 2.04, sensorH: 1.08 },
    "RED_Dragon (full frame)": { sensorW: 3.072, sensorH: 1.58 },
    "RED_MysteriumX S35": { sensorW: 2.765, sensorH: 1.3825 },
    "RED_WeaponS35 HD": { sensorW: 1.577, sensorH: 0.86735 },
    "RED_WeaponS35 5.5k (full frame)": { sensorW: 2.055822, sensorH: 1.076094 },
    "RED_WeaponS35 8k (full frame)": { sensorW: 2.990231, sensorH: 1.57688 },
    "SONY F55": { sensorW: 2.404144, sensorH: 1.26781 },
    "SONY F65": { sensorW: 2.477075, sensorH: 1.30627 },
    "SONY Venice2 (full frame)": { sensorW: 3.593332, sensorH: 2.395554 },
    "SONY Venice2 5.8k": { sensorW: 2.410176, sensorH: 2.019854 }
};

const lensData = [
    "ZEISS Supreme 15mm", "ZEISS Supreme 18mm", "ZEISS Supreme 21mm",
    "ZEISS Supreme 25mm", "ZEISS Supreme 29mm", "ZEISS Supreme 35mm",
    "ZEISS Supreme 50mm", "ZEISS Supreme 85mm", "ZEISS Supreme 100mm",
    "ZEISS Supreme 135mm", "ZEISS Supreme 150mm", "ZEISS Supreme 200mm",
    "ZEISS CP3 15mm", "ZEISS CP3 18mm", "ZEISS CP3 21mm", "ZEISS CP3 25mm",
    "ZEISS CP3 28mm", "ZEISS CP3 35mm", "ZEISS CP3 50mm", "ZEISS CP3 85mm",
    "ZEISS CP3 100mm", "ZEISS CP3 135mm", "ZEISS CP2-SS 35mm",
    "ZEISS CP2 15mm", "ZEISS CP2 MACRO 50mm", "ARRIFLEX-ZEISS MK 18mm",
    "ARRIFLEX-ZEISS MK 25mm", "ARRIFLEX-ZEISS MK 35mm", "ARRIFLEX-ZEISS MK 50mm",
    "ARRIFLEX-ZEISS MK 65mm", "ARRIFLEX-ZEISS MK 85mm", "ARRI-ZEISS Master 12mm",
    "ARRI-ZEISS Master 14mm", "ARRI-ZEISS Master 16mm", "ARRI-ZEISS Master 18mm",
    "ARRI-ZEISS Master 21mm", "ARRI-ZEISS Master 25mm", "ARRI-ZEISS Master 27mm",
    "ARRI-ZEISS Master 32mm", "ARRI-ZEISS Master 35mm", "ARRI-ZEISS Master 40mm",
    "ARRI-ZEISS Master 50mm", "ARRI-ZEISS Master 65mm", "ARRI-ZEISS Master 75mm",
    "ARRI-ZEISS Master 100mm", "ARRI-ZEISS Master 135mm", "ARRI-ZEISS Master 150mm",
    "ARRI-ZEISS Master MACRO 100mm"
];

const cameraSelect = document.getElementById("camera");
const sensorWidthInput = document.getElementById("sensorWidth");
const sensorHeightInput = document.getElementById("sensorHeight");
const lensSelect = document.getElementById("lens");
const outputElement = document.getElementById("output");
const runButton = document.getElementById("runInference");

const inputFeatures = ["k1", "k2", "sensorWidth", "sensorHeight", "distance"];

// Populate camera dropdown
Object.keys(cameraData).sort().forEach(camera => {
    const option = document.createElement("option");
    option.value = camera;
    option.textContent = camera;
    cameraSelect.appendChild(option);
});

// Populate lens dropdown alphabetically
lensData.sort((a, b) => a.localeCompare(b)).forEach(lens => {
    const option = document.createElement("option");
    option.value = lens;
    option.textContent = lens;
    lensSelect.appendChild(option);
});

// Update sensor width and height based on selected camera
cameraSelect.addEventListener("change", () => {
    const selectedCamera = cameraSelect.value;
    if (selectedCamera && cameraData[selectedCamera]) {
        sensorWidthInput.value = cameraData[selectedCamera].sensorW.toFixed(3);
        sensorHeightInput.value = cameraData[selectedCamera].sensorH.toFixed(3);
    } else {
        sensorWidthInput.value = "";
        sensorHeightInput.value = "";
    }
});

// Prefill focal length based on lens selection
lensSelect.addEventListener("change", () => {
    const selectedLens = lensSelect.value;
    const focalMatch = selectedLens.match(/(\d+)mm$/);
    document.getElementById("focalLength").value = focalMatch ? parseInt(focalMatch[1], 10) : "";
});



function parseAndValidateFloat(inputFieldId, min = -Infinity, max = Infinity) {
    const inputField = document.getElementById(inputFieldId);
    if (!inputField) return { valid: false, value: null, error: `Field '${inputFieldId}' not found` };

    const trimmedValue = inputField.value.trim(); // Trim whitespace

    const value = parseFloat(trimmedValue);

    if (isNaN(value)) {
        inputField.focus(); // Highlight the element
        inputField.select(); // Select its content
        return { valid: false, value: null, error: `Invalid number in field '${inputFieldId}'` };
    }

    if (value < min || value > max) {
        inputField.focus(); // Highlight the element
        inputField.select(); // Select its content
        return {
            valid: false,
            value,
            error: `Value '${value}' in field '${inputFieldId}' out of range (${min} to ${max})`
        };
    }

    return { valid: true, value, error: null };
}

function parseAndValidateInt(inputFieldId, min = -Infinity, max = Infinity) {
    const inputField = document.getElementById(inputFieldId);
    if (!inputField) return { valid: false, value: null, error: `Field '${inputFieldId}' not found` };

    const trimmedValue = inputField.value.trim(); // Trim whitespace
    const value = parseInt(trimmedValue);

    if (isNaN(value)) {
        inputField.focus(); // Highlight the element
        inputField.select(); // Select its content
        return { valid: false, value: null, error: `Invalid number in field '${inputFieldId}'` };
    }

    if (value < min || value > max) {
        inputField.focus(); // Highlight the element
        inputField.select(); // Select its content
        return {
            valid: false,
            value,
            error: `Value '${value}' in field '${inputFieldId}' out of range (${min} to ${max})`
        };
    }

    return { valid: true, value, error: null };
}



// Utility function to load ONNX model and run inference
async function loadAndRunModel(modelPath, inputValues) {
    const session = await ort.InferenceSession.create(modelPath);
    const inputTensor = new ort.Tensor('float32', new Float32Array(inputValues), [1, 5]);
    const results = await session.run({ "scaler_float_input": inputTensor });
    return results["xgb_variable"].data[0];
}

// Run inference on button click
runButton.addEventListener("click", async () => {
    try {
        // Validate and prepare input data
        const values = inputFeatures.map(id => {
            const result = parseAndValidateFloat(id);
            if (!result.valid) throw new Error(result.error || `Invalid value for ${id}.`);
            return result.value;
        });

        // Retrieve and validate focal length
        const focalLengthResult = parseAndValidateInt("focalLength", 1);
        if (!focalLengthResult.valid) throw new Error(focalLengthResult.error || "Invalid focal length.");
        const focalLength = focalLengthResult.value;

        // Validate lens availability
        if (!lensData.some(lens => lens.includes(`${focalLength}mm`))) {
            throw new Error(`No model available for ${focalLength}mm.`);
        }

        // Run inference for K1 and K2
        const modelPathBase = `./${focalLength}mm`;
        const [outputData1, outputData2] = await Promise.all([
            loadAndRunModel(`${modelPathBase}_k1.onnx`, values),
            loadAndRunModel(`${modelPathBase}_k2.onnx`, values)
        ]);

        // Display the result
        outputElement.textContent = `K1: ${outputData1.toFixed(4)} K2: ${outputData2.toFixed(4)}`;

    } catch (error) {
        outputElement.textContent = `Error: ${error.message || "An unexpected error occurred."}`;
    }
});


