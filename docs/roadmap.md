# BlackMamba ScrewVision Roadmap

> From screw detection to industrial inspection intelligence.

Creator: **Iyari Cancino Gomez**, alias **BlackMamba**.

## Current State

```text
Latest release: v0.4.0
Current product shape: mobile-friendly inspection demo
```

ScrewVision can currently:

- accept image upload through API or dashboard
- capture still images from a browser camera
- analyze imagery with deterministic OpenCV fallback logic
- return bounding boxes, geometry, material estimate, wear, confidence, quality score, and inspection result
- record detection telemetry in SQLite
- render telemetry, roadmap, and latest analysis in the dashboard
- publish release assets through GitHub Actions

## Release History

| Version | Status | Theme | Outcome |
| --- | --- | --- | --- |
| `v0.1.0` | Released | Foundation | FastAPI, runtime, OpenCV analysis, telemetry, tests, dashboard shell |
| `v0.2.0` | Released | Visual Detection Layer | Detector abstraction, bbox contract, CI/release automation |
| `v0.3.0` | Released | Mobile Camera Capture | Browser camera capture, mobile upload fallback, LAN demo flow |
| `v0.3.1` | Released | Go-To-Market Kit | Demo script, positioning, outreach copy, pricing anchors |
| `v0.4.0` | Released | Quality Inspection | `quality_score`, `PASS` / `REVIEW` / `FAIL`, inspection telemetry |

## Next Releases

### v0.5.0 - Multi-Class Industrial Detection

Goal: expand from screw-focused analysis to basic industrial part classification.

Initial classes:

```text
bolt
screw
nut
washer
unknown
```

Deliverables:

| Component | Status |
| --- | --- |
| Multi-class schema | Planned |
| Class-specific heuristic rules | Planned |
| Dashboard class breakdown | Planned |
| Telemetry class counts | Planned |
| API contract tests | Planned |

### v0.6.0 - Dataset Factory

Goal: create the first repeatable data workflow for future model training.

Structure:

```text
datasets/
  raw/
  labeled/
  train/
  val/
  test/
```

Scripts:

```text
tools/prepare_dataset.py
tools/evaluate.py
tools/train_detector.py
```

Deliverables:

| Component | Status |
| --- | --- |
| Dataset folder contract | Planned |
| Label manifest format | Planned |
| Train/val/test splitter | Planned |
| Evaluation report | Planned |

### v0.7.0 - Calibration and Measurement

Goal: move from pixel geometry toward real-world measurements.

Deliverables:

| Component | Status |
| --- | --- |
| Pixel-to-mm calibration | Planned |
| Reference object workflow | Planned |
| Measurement confidence | Planned |
| Dashboard measurement display | Planned |

### v1.0.0 - Mechanical Intelligence Platform

Goal: graduate from prototype to a platform-style runtime for lightweight industrial inspection.

Expected baseline:

- multi-class inspection
- mobile capture
- reliable telemetry
- calibration workflow
- dataset pipeline
- release automation
- documented commercial demo

## Long-Term Platform Phases

The long-term architecture progression is:

```text
Physics -> Vision -> Semantics -> Autonomy
```

### Phase 0 - Genesis Runtime

Goal: create the foundational recognition and inspection pipeline.

Completed or in progress:

- image upload
- mobile still capture
- FastAPI detection endpoint
- React/Vite dashboard
- OpenCV fallback detector
- bounding box response contract
- quality inspection scoring
- SQLite telemetry
- CI and release automation

Planned:

- trained detector backend
- dataset factory
- multi-object support

### Phase 1 - Semantic Morphology Engine

Goal: move beyond labels into morphology understanding.

Features:

- head topology
- threading geometry
- shaft proportions
- contour signatures
- segmentation overlays
- defect heatmaps

### Phase 2 - Industrial Intelligence Layer

Goal: understand industrial context and hardware ecosystems.

Features:

- automatic counting
- stock estimation
- defect reports
- hardware analytics
- compatibility reasoning
- hardware knowledge graph

### Phase 3 - Edge AI Runtime

Goal: deploy industrial intelligence directly on edge devices.

Targets:

- Raspberry Pi
- NVIDIA Jetson
- industrial PCs
- ARM edge systems

### Phase 4 - Robotics Integration

Goal: connect ScrewVision to robotic systems.

Features:

- object localization
- grasp-point prediction
- sorting workflows
- guided assembly
- ROS2 or PLC integration

### Phase 5 - Mechanical Cognition Engine

Goal: reason about mechanical systems, not only detected objects.

Features:

- assembly logic
- maintenance risk
- failure probability
- mechanical twin runtime

### Phase 6 - Cybernetic Factory Runtime

Goal: distributed industrial cognition.

Features:

- multi-camera systems
- event streaming
- telemetry mesh
- predictive maintenance
- production health dashboard

## Recommended Stack Evolution

| Layer | Current | Future |
| --- | --- | --- |
| Detection | OpenCV heuristics | YOLO / RT-DETR / custom model |
| Segmentation | Planned | SAM / YOLO-Seg |
| Geometry | OpenCV pixels | Calibrated measurements |
| Runtime | FastAPI | FastAPI + async streaming |
| Dashboard | React + Tailwind | Mobile-first inspection console |
| Telemetry | SQLite | PostgreSQL / Redis Streams |
| Edge | Local dev machine | Jetson / Raspberry Pi / industrial PC |
| Robotics | Planned | ROS2 |

## Product Thesis

ScrewVision should not sell "AI" as the product. It should sell inspection outcomes:

```text
Detect parts.
Count production.
Flag defects.
Score quality.
Generate visual reports.
```
