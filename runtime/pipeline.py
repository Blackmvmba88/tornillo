from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from ai.classifier import HeuristicScrewClassifier
from runtime.schemas import DetectionResult, RuntimeMode


class ScrewVisionRuntime:
    def __init__(self, mode: RuntimeMode = "detection") -> None:
        self.mode = mode
        self.classifier = HeuristicScrewClassifier()

    def analyze_image_path(self, path: Path) -> DetectionResult:
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")
        payload = path.read_bytes()
        return self.analyze_image_bytes(payload, source=str(path))

    def analyze_image_bytes(self, payload: bytes, source: str = "upload") -> DetectionResult:
        image = self._decode(payload)
        return self.classifier.classify(image=image, source=source, mode=self.mode)

    @staticmethod
    def _decode(payload: bytes) -> np.ndarray:
        buffer = np.frombuffer(payload, dtype=np.uint8)
        image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Unable to decode image payload.")
        return image
