from __future__ import annotations

from pathlib import Path
from typing import Protocol

import cv2
import numpy as np

from runtime.schemas import (
    BoundingBox,
    DetectionResult,
    GeometryEstimate,
    RuntimeMode,
    ScrewClassification,
)


class Detector(Protocol):
    name: str
    model_name: str | None

    def detect(self, image: np.ndarray, source: str, mode: RuntimeMode) -> DetectionResult:
        ...


class OpenCVDetector:
    """Deterministic fallback detector used before trained model weights exist."""

    name = "opencv"
    model_name = "contour-heuristic"

    def detect(self, image: np.ndarray, source: str, mode: RuntimeMode) -> DetectionResult:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            classification = ScrewClassification(confidence=0.0)
            return DetectionResult(
                source=source,
                mode=mode,
                detected=False,
                detector=self.name,
                model=self.model_name,
                screw_type=classification.screw_family,
                material=classification.material_estimate,
                wear=classification.wear_score,
                confidence=classification.confidence,
                quality_score=0.0,
                inspection_result="FAIL",
                bbox=None,
                classification=classification,
                geometry=GeometryEstimate(),
                notes=["No contours detected."],
            )

        contour = max(contours, key=cv2.contourArea)
        area = float(cv2.contourArea(contour))
        x, y, w, h = cv2.boundingRect(contour)
        length = float(max(w, h))
        width = float(min(w, h))
        aspect_ratio = length / width if width else 0.0
        detected = area > 80 and length > 12

        confidence = self._confidence(area, aspect_ratio, detected)
        bbox = (
            BoundingBox(
                x=int(x),
                y=int(y),
                width=int(w),
                height=int(h),
                confidence=confidence,
            )
            if detected
            else None
        )

        geometry = GeometryEstimate(
            head_diameter_px=round(width, 2),
            shaft_diameter_px=round(width * 0.55, 2),
            length_px=round(length, 2),
            aspect_ratio=round(aspect_ratio, 3),
            contour_area_px=round(area, 2),
        )

        classification = ScrewClassification(
            screw_family=self._family(aspect_ratio),
            head_type=self._head_type(gray[y : y + h, x : x + w], aspect_ratio),
            thread_type=self._thread_type(edges[y : y + h, x : x + w], aspect_ratio),
            material_estimate=self._material(image[y : y + h, x : x + w]),
            wear_score=self._wear_score(image[y : y + h, x : x + w]),
            confidence=confidence,
        )

        flags = []
        if classification.wear_score > 0.55:
            flags.append("possible_corrosion_or_surface_wear")
        if aspect_ratio < 1.4 and detected:
            flags.append("short_fastener_or_top_down_view")

        quality_score = self._quality_score(
            detected=detected,
            confidence=classification.confidence,
            wear_score=classification.wear_score,
            defect_count=len(flags),
        )
        inspection_result = self._inspection_result(quality_score)

        notes = ["OpenCV fallback analysis; replace with YOLO backend when trained weights exist."]
        if mode in {"lab", "semantic"}:
            notes.append("Lab metrics include contour-derived geometry in pixels.")
        if mode == "semantic":
            notes.append("Semantic compatibility reasoning is scaffolded for future graph logic.")

        return DetectionResult(
            source=source,
            mode=mode,
            detected=detected,
            detector=self.name,
            model=self.model_name,
            screw_type=classification.screw_family,
            material=classification.material_estimate,
            wear=classification.wear_score,
            confidence=classification.confidence,
            quality_score=quality_score,
            inspection_result=inspection_result,
            bbox=bbox,
            classification=classification,
            geometry=geometry,
            defect_flags=flags,
            notes=notes,
        )

    classify = detect

    @staticmethod
    def _family(aspect_ratio: float) -> str:
        if aspect_ratio >= 3.0:
            return "screw_or_bolt"
        if aspect_ratio >= 1.5:
            return "short_screw_or_fastener"
        return "washer_nut_or_head_view"

    @staticmethod
    def _head_type(region: np.ndarray, aspect_ratio: float) -> str:
        if region.size == 0:
            return "unknown"
        circles = cv2.HoughCircles(
            region,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=20,
            param1=80,
            param2=20,
            minRadius=4,
            maxRadius=80,
        )
        if circles is not None:
            return "round_or_phillips_candidate"
        if aspect_ratio >= 3.0:
            return "elongated_side_profile"
        return "flat_or_hex_candidate"

    @staticmethod
    def _thread_type(region: np.ndarray, aspect_ratio: float) -> str:
        if region.size == 0 or aspect_ratio < 2.0:
            return "unknown"
        vertical_density = float(np.count_nonzero(region)) / float(region.size)
        if vertical_density > 0.12:
            return "coarse_or_visible_thread"
        return "fine_or_low_visibility_thread"

    @staticmethod
    def _material(region: np.ndarray) -> str:
        if region.size == 0:
            return "unknown"
        mean_bgr = region.reshape(-1, 3).mean(axis=0)
        blue, green, red = mean_bgr
        if red > green * 1.15 and red > blue * 1.2:
            return "brass_or_rust_tinted"
        if np.mean(mean_bgr) > 175:
            return "bright_steel_or_aluminum"
        return "dark_steel_or_coated"

    @staticmethod
    def _wear_score(region: np.ndarray) -> float:
        if region.size == 0:
            return 0.0
        hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        saturation = float(hsv[:, :, 1].mean()) / 255.0
        value_variance = float(hsv[:, :, 2].std()) / 128.0
        return round(min(1.0, saturation * 0.55 + value_variance * 0.45), 3)

    @staticmethod
    def _confidence(area: float, aspect_ratio: float, detected: bool) -> float:
        if not detected:
            return 0.0
        area_score = min(1.0, area / 4000.0)
        shape_score = min(1.0, max(0.2, aspect_ratio / 4.0))
        return round((area_score * 0.55) + (shape_score * 0.45), 3)

    @staticmethod
    def _quality_score(detected: bool, confidence: float, wear_score: float, defect_count: int) -> float:
        if not detected:
            return 0.0
        wear_penalty = wear_score * 0.35
        defect_penalty = min(0.3, defect_count * 0.15)
        score = confidence - wear_penalty - defect_penalty
        return round(max(0.0, min(1.0, score)), 3)

    @staticmethod
    def _inspection_result(quality_score: float) -> str:
        if quality_score >= 0.72:
            return "PASS"
        if quality_score >= 0.45:
            return "REVIEW"
        return "FAIL"


class YoloDetectorConfig:
    def __init__(self, weights_path: Path = Path("models/screwvision-yolov8.pt")) -> None:
        self.weights_path = weights_path


class YoloDetector:
    """YOLO adapter shell; activated only when weights and integration are present."""

    name = "yolo"
    model_name = "yolov8"

    def __init__(self, config: YoloDetectorConfig | None = None) -> None:
        self.config = config or YoloDetectorConfig()

    @property
    def available(self) -> bool:
        return self.config.weights_path.exists()

    @property
    def ready(self) -> bool:
        return False

    def detect(self, image: np.ndarray, source: str, mode: RuntimeMode) -> DetectionResult:
        raise NotImplementedError("YOLO integration is pending trained weights and ultralytics wiring.")


def get_detector() -> Detector:
    yolo = YoloDetector()
    if yolo.available and yolo.ready:
        return yolo
    return OpenCVDetector()
