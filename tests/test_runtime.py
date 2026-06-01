from __future__ import annotations

import cv2
import numpy as np

from runtime.pipeline import ScrewVisionRuntime


def encode_test_screw() -> bytes:
    image = np.zeros((180, 260, 3), dtype=np.uint8)
    cv2.rectangle(image, (70, 80), (210, 102), (210, 210, 210), -1)
    cv2.circle(image, (55, 91), 24, (230, 230, 230), -1)
    ok, encoded = cv2.imencode(".jpg", image)
    assert ok
    return encoded.tobytes()


def test_runtime_detects_synthetic_screw() -> None:
    runtime = ScrewVisionRuntime(mode="lab")
    result = runtime.analyze_image_bytes(encode_test_screw(), source="synthetic.jpg")

    assert result.detected is True
    assert result.mode == "lab"
    assert result.detector == "opencv"
    assert result.bbox is not None
    assert result.bbox.width > 0
    assert result.bbox.height > 0
    assert result.geometry.length_px > 100
    assert result.confidence > 0
    assert result.classification.confidence == result.confidence
