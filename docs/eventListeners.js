import * as common from "./common.js";

export function populateCameraDropdown(cameraSelect) {
    Object.keys(common.cameraData)
        .sort()
        .forEach(camera => {
            const option = document.createElement("option");
            option.value = camera;
            option.textContent = camera;
            cameraSelect.appendChild(option);
        });
}

export function populateLensDropdown(lensSelect) {
    common.lensData
        // .sort((a, b) => a.localeCompare(b))
        .forEach(lens => {
            const option = document.createElement("option");
            option.value = lens;
            option.textContent = lens;
            lensSelect.appendChild(option);
        });
}

export function setupCameraChangeListener(cameraSelect, sensorWidthInput, sensorHeightInput) {
    cameraSelect.addEventListener("change", () => {
        const selectedCamera = cameraSelect.value;
        if (selectedCamera && common.cameraData[selectedCamera]) {
            sensorWidthInput.value = common.cameraData[selectedCamera].sensorW.toFixed(3);
            sensorHeightInput.value = common.cameraData[selectedCamera].sensorH.toFixed(3);
        } else {
            sensorWidthInput.value = "";
            sensorHeightInput.value = "";
        }
    });
}

export function setupLensChangeListener(lensSelect, focalLengthInput) {
    lensSelect.addEventListener("change", () => {
        const selectedLens = lensSelect.value;
        const focalMatch = selectedLens.match(/(\d+)mm$/);
        focalLengthInput.value = focalMatch ? parseInt(focalMatch[1], 10) : "";
    });
}

export function setupSliderAndDistanceListeners(slider, distanceInput) {
    slider.addEventListener("input", () => {
        const logValue = common.linearToLogarithmic(slider.value);
        distanceInput.value = logValue.toFixed(0);
    });

    distanceInput.addEventListener("input", () => {
        let logValue = parseFloat(distanceInput.value);
        if (logValue < common.minValue) logValue = common.minValue;
        if (logValue > common.maxValue) logValue = common.maxValue;

        const sliderValue = common.logarithmicToLinear(logValue);
        slider.value = sliderValue;
    });
}
