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
    "ARRI-ZEISS Master 12mm", "ARRI-ZEISS Master 14mm", "ARRI-ZEISS Master 16mm",
    "ARRI-ZEISS Master 18mm", "ARRI-ZEISS Master 21mm", "ARRI-ZEISS Master 25mm",
    "ARRI-ZEISS Master 27mm", "ARRI-ZEISS Master 32mm", "ARRI-ZEISS Master 35mm",
    "ARRI-ZEISS Master 40mm", "ARRI-ZEISS Master 50mm", "ARRI-ZEISS Master 65mm",
    "ARRI-ZEISS Master 75mm", "ARRI-ZEISS Master 100mm", "ARRI-ZEISS Master 135mm",
    "ARRI-ZEISS Master 150mm", "ARRI-ZEISS Master MACRO 100mm",
    "ARRIFLEX-ZEISS MK 18mm", "ARRIFLEX-ZEISS MK 25mm", "ARRIFLEX-ZEISS MK 35mm",
    "ARRIFLEX-ZEISS MK 50mm", "ARRIFLEX-ZEISS MK 65mm", "ARRIFLEX-ZEISS MK 85mm",
    "ZEISS CP2 15mm", "ZEISS CP2-SS 35mm", "ZEISS CP2 MACRO 50mm",
    "ZEISS CP3 15mm", "ZEISS CP3 18mm", "ZEISS CP3 21mm", "ZEISS CP3 25mm",
    "ZEISS CP3 28mm", "ZEISS CP3 35mm", "ZEISS CP3 50mm", "ZEISS CP3 85mm",
    "ZEISS CP3 100mm", "ZEISS CP3 135mm",
    "ZEISS Supreme 15mm", "ZEISS Supreme 18mm", "ZEISS Supreme 21mm",
    "ZEISS Supreme 25mm", "ZEISS Supreme 29mm", "ZEISS Supreme 35mm",
    "ZEISS Supreme 50mm", "ZEISS Supreme 85mm", "ZEISS Supreme 100mm",
    "ZEISS Supreme 135mm", "ZEISS Supreme 150mm", "ZEISS Supreme 200mm"
];


const minValue = 1, maxValue = 10000, minSlider = 0, maxSlider = 10000;

function formatLensString(input) {
    return input
        .replace(/\s+/g, '_')                 // Replace spaces with underscores
        .replace(/(\d+)mm/, (match, num) =>  // Match number followed by "mm"
            `${num.padStart(3, '0')}mm`      // Pad the number to 3 digits
        )
        .replace(/_+/g, '_');                // Ensure no double underscores
}

function populateDropdown(selectElementId, data, isObject = false) {
    const dropdown = document.getElementById(selectElementId);
    if (!dropdown) return;

    dropdown.innerHTML = "";
    Object.entries(data).forEach(([key, value]) => {
        const option = document.createElement("option");
        option.value = isObject ? key : value;
        option.textContent = key;
        dropdown.appendChild(option);
    });
}

function linearToLogarithmic(linearValue) {
    const logMin = Math.log(minValue);
    const logMax = Math.log(maxValue);
    const scale = (logMax - logMin) / (maxSlider - minSlider);
    return Math.exp(logMin + scale * (linearValue - minSlider));
}

function logarithmicToLinear(logValue) {
    const logMin = Math.log(minValue);
    const logMax = Math.log(maxValue);
    const scale = (maxSlider - minSlider) / (logMax - logMin);
    return minSlider + scale * (Math.log(logValue) - logMin);
}

function parseAndValidateNumber(inputFieldId, type = 'float', min = -Infinity, max = Infinity) {
    const inputField = document.getElementById(inputFieldId);
    if (!inputField) return { valid: false, value: null, error: `Field '${inputFieldId}' not found` };

    const trimmedValue = inputField.value.trim();
    const value = type === 'int' ? parseInt(trimmedValue) : parseFloat(trimmedValue);

    if (isNaN(value) || value < min || value > max) {
        inputField.focus();
        inputField.select();
        return { valid: false, value: null, error: `Invalid value in '${inputFieldId}' (${min} - ${max})` };
    }

    return { valid: true, value };
}

// Validate focal length against lensData
function validateFocalLength(focalLength) {
    const lensFound = lensData.some(lens => lens.includes(`${focalLength}mm`));
    return lensFound ? { valid: true } : { valid: false, error: `No model available for ${focalLength}mm.` };
}

// Load and run ONNX model
async function loadAndRunModel(modelPath, inputValues) {
    if (!modelPath) throw new Error("Model path is not specified.");

        // test if modelPath exists
        const response = await fetch(modelPath);
        if (!response.ok) throw new Error(`Model not found: ${modelPath}`);

        const session = await ort.InferenceSession.create(modelPath);
        const inputTensor = new ort.Tensor('float32', new Float32Array(inputValues), [1, inputValues.length]);
        const results = await session.run({ "scaler_float_input": inputTensor });
        return results["xgb_variable"].data[0];
}


// Export functions and data
export {
    cameraData,
    lensData,
    populateDropdown,
    formatLensString,
    linearToLogarithmic,
    logarithmicToLinear,
    parseAndValidateNumber,
    validateFocalLength,
    loadAndRunModel
};

// Default export for convenience
export default {
    cameraData,
    lensData,
    populateDropdown,
    formatLensString,
    linearToLogarithmic,
    logarithmicToLinear,
    parseAndValidateNumber,
    validateFocalLength,
    loadAndRunModel
};
