from __future__ import annotations

import cv2
import numpy as np

from ai.detectors import OpenCVDetector
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
    assert result.quality_score > 0
    assert result.inspection_result in {"PASS", "REVIEW", "FAIL"}
    assert result.classification.confidence == result.confidence


def test_inspection_result_thresholds() -> None:
    detector = OpenCVDetector()

    assert detector._inspection_result(0.72) == "PASS"
    assert detector._inspection_result(0.45) == "REVIEW"
    assert detector._inspection_result(0.44) == "FAIL"


def test_quality_score_penalizes_wear_and_defects() -> None:
    detector = OpenCVDetector()

    clean_score = detector._quality_score(detected=True, confidence=0.9, wear_score=0.0, defect_count=0)
    worn_score = detector._quality_score(detected=True, confidence=0.9, wear_score=1.0, defect_count=2)

    assert clean_score == 0.9
    assert worn_score < clean_score
    assert detector._quality_score(detected=False, confidence=0.9, wear_score=0.0, defect_count=0) == 0.0
