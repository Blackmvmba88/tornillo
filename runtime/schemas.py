from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


RuntimeMode = Literal["detection", "lab", "semantic"]


class GeometryEstimate(BaseModel):
    head_diameter_px: float = 0.0
    shaft_diameter_px: float = 0.0
    length_px: float = 0.0
    aspect_ratio: float = 0.0
    contour_area_px: float = 0.0


class ScrewClassification(BaseModel):
    screw_family: str = "unknown"
    head_type: str = "unknown"
    thread_type: str = "unknown"
    material_estimate: str = "unknown"
    wear_score: float = Field(default=0.0, ge=0.0, le=1.0)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class DetectionResult(BaseModel):
    source: str
    mode: RuntimeMode
    detected: bool
    classification: ScrewClassification
    geometry: GeometryEstimate
    defect_flags: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
