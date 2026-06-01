# ScrewVision Architecture

```text
Camera or Image Upload
    -> Frame Acquisition Runtime
    -> Detector Backend
    -> Semantic Morphology Analyzer
    -> Industrial Classification Runtime
    -> Telemetry Store
    -> API and Dashboard
```

## First-Cut Runtime

The current runtime uses deterministic OpenCV contour analysis to extract geometry and produce a conservative classification. This makes the repo testable before model training.

## YOLO Integration Point

Add trained weights under `models/` and replace or compose `HeuristicScrewClassifier` with a YOLO adapter in `ai/detectors.py`.

## Telemetry

Every API detection records a normalized event in SQLite. The summary endpoint powers dashboard metrics and can later be upgraded to PostgreSQL.
