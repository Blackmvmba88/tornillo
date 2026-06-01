from __future__ import annotations

from pathlib import Path


class YoloDetectorConfig:
    def __init__(self, weights_path: Path = Path("models/screwvision-yolov8.pt")) -> None:
        self.weights_path = weights_path


class YoloDetector:
    """Placeholder adapter for future ultralytics YOLOv8 integration."""

    def __init__(self, config: YoloDetectorConfig | None = None) -> None:
        self.config = config or YoloDetectorConfig()

    @property
    def available(self) -> bool:
        return self.config.weights_path.exists()
