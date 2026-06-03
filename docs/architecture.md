# ScrewVision Architecture

Creator: **Iyari Cancino Gomez**, alias **BlackMamba**.

## Runtime Flow

```text
Image upload or mobile camera capture
    -> FastAPI /detect endpoint
    -> ScrewVisionRuntime
    -> Detector backend
    -> Classification and geometry estimates
    -> Quality inspection scoring
    -> SQLite telemetry
    -> Dashboard and API response
```

## Main Modules

| Module | Responsibility |
| --- | --- |
| `api/main.py` | FastAPI app, CORS, detection endpoint, telemetry endpoint, roadmap endpoint |
| `api/roadmap.py` | Machine-readable roadmap rendered by dashboard |
| `runtime/pipeline.py` | Image decoding and runtime orchestration |
| `runtime/schemas.py` | Pydantic contracts for detection, geometry, bbox, inspection result |
| `ai/detectors.py` | Detector protocol, OpenCV fallback, YOLO adapter shell |
| `telemetry/store.py` | SQLite detection event storage and summary aggregation |
| `webui/src/App.jsx` | Dashboard, mobile capture, upload, latest result, telemetry, roadmap |
| `scripts/dev.py` | Combined API + WebUI local runner |

## Detector Boundary

The API should not know which detector implementation is active.

```text
API
  -> ScrewVisionRuntime
    -> Detector protocol
      -> OpenCVDetector
      -> YoloDetector
      -> FutureDetector
```

Current active detector:

```text
OpenCVDetector / contour-heuristic
```

Future detector:

```text
YoloDetector / yolov8
```

The `YoloDetector` remains inactive until model inference wiring is implemented.

## Detection Contract

`DetectionResult` is the stable cross-layer contract.

Important fields:

| Field | Meaning |
| --- | --- |
| `detected` | Whether a candidate object was detected |
| `detector` | Active detector family, e.g. `opencv` |
| `model` | Detector model name or heuristic name |
| `screw_type` | Current object-family classification |
| `material` | Surface/material estimate |
| `wear` | Wear/corrosion signal from image features |
| `confidence` | Detector confidence |
| `quality_score` | Inspection score from `0.0` to `1.0` |
| `inspection_result` | `PASS`, `REVIEW`, or `FAIL` |
| `bbox` | Bounding box in image pixels |
| `geometry` | Pixel-level shape estimates |
| `defect_flags` | Conservative warnings from runtime analysis |

## Inspection Scoring

The current scoring system is deterministic:

```text
quality_score = confidence - wear_penalty - defect_penalty
```

Thresholds:

| Score | Result |
| --- | --- |
| `>= 0.72` | `PASS` |
| `>= 0.45` and `< 0.72` | `REVIEW` |
| `< 0.45` | `FAIL` |

## Telemetry

Every successful `POST /detect` records the full payload plus summary columns:

- source
- mode
- detector
- detected
- family
- head type
- confidence
- quality score
- inspection result
- bbox
- JSON payload

Local database:

```text
telemetry/screwvision.sqlite
```

The SQLite file is runtime state and ignored by git.

## Dashboard

The WebUI is intentionally an operator surface, not a marketing landing page.

Current views:

- event count
- detection count
- average confidence
- upload button
- camera capture button
- latest image preview
- bounding box overlay
- detector/model badge
- inspection badge
- quality metric
- telemetry signals
- roadmap cards

## Local Network Demo

`scripts/dev.py` binds API and WebUI to `0.0.0.0`.

This allows a phone on the same network to open:

```text
http://YOUR_MACHINE_IP:5173
```

The dashboard derives API host from the browser host, so it calls:

```text
http://YOUR_MACHINE_IP:8000
```

## Non-Goals For Current Runtime

These are intentionally not implemented yet:

- continuous video inference
- trained YOLO inference
- calibrated real-world measurements
- production authentication
- cloud storage
- multi-camera event streaming
- robot control
