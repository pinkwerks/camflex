import * as common from "./common.js";

const inputFeatures = ["k1", "k2", "sensorWidth", "sensorHeight", "distance"];

// Run inference on button click
common.runButton.addEventListener("click", async () => {
    // Clear the output element
    outputElement.textContent = ""; // Clear previous output
    
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

        const k1_model = `./${focalLength}mm_k1.onnx`;
        const k2_model = `./${focalLength}mm_k2.onnx`;

        // Run inference for K1 and K2
        const modelPathBase = `./${focalLength}mm`;
        const [outputData1, outputData2] = await Promise.all([
            loadAndRunModel(`${k1_model}`, values),
            loadAndRunModel(`${k2_model}`, values)
        ]);

        outputElement.textContent = `Loaded model ${k1_model}...\n`;
        outputElement.textContent += `Loaded model ${k2_model}...\n`;
        outputElement.textContent += `\n`;

        // Display the result
        outputElement.textContent += `K1: ${outputData1.toFixed(4)}\n`;
        outputElement.textContent += `K2: ${outputData2.toFixed(4)}`;

    } catch (error) {
        outputElement.textContent = `Error: ${error.message || "An unexpected error occurred."}`;
    }
});


