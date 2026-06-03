# ScrewVision API and Runtime Reference

Creator: **Iyari Cancino Gomez**, alias **BlackMamba**.

## HTTP Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Runtime health check |
| `POST` | `/detect` | Analyze an uploaded image |
| `GET` | `/telemetry/summary` | Return aggregate detection telemetry |
| `GET` | `/roadmap` | Return the machine-readable product roadmap |

## `GET /health`

Response:

```json
{
  "status": "ok",
  "runtime": "screwvision"
}
```

## `POST /detect`

Request:

```bash
curl -X POST http://127.0.0.1:8000/detect -F image=@screw.jpg
```

Response contract:

```json
{
  "source": "screw.jpg",
  "mode": "detection",
  "detected": true,
  "detector": "opencv",
  "model": "contour-heuristic",
  "screw_type": "screw_or_bolt",
  "material": "bright_steel_or_aluminum",
  "wear": 0.12,
  "confidence": 0.71,
  "quality_score": 0.67,
  "inspection_result": "REVIEW",
  "bbox": {
    "x": 10,
    "y": 20,
    "width": 140,
    "height": 24,
    "confidence": 0.71
  },
  "classification": {
    "screw_family": "screw_or_bolt",
    "head_type": "round_or_phillips_candidate",
    "thread_type": "fine_or_low_visibility_thread",
    "material_estimate": "bright_steel_or_aluminum",
    "wear_score": 0.12,
    "confidence": 0.71
  },
  "geometry": {
    "head_diameter_px": 24.0,
    "shaft_diameter_px": 13.2,
    "length_px": 140.0,
    "aspect_ratio": 5.83,
    "contour_area_px": 1000.0
  },
  "defect_flags": [],
  "notes": []
}
```

## `GET /telemetry/summary`

Response:

```json
{
  "total_events": 10,
  "detected_events": 9,
  "average_confidence": 0.82,
  "top_families": [{ "family": "screw_or_bolt", "count": 8 }],
  "detectors": [{ "detector": "opencv", "count": 10 }],
  "inspection_results": [{ "result": "PASS", "count": 7 }]
}
```

## `GET /roadmap`

Response shape:

```json
{
  "vision": "Physics -> Vision -> Semantics -> Autonomy",
  "phases": [],
  "stack_evolution": {}
}
```

The roadmap is defined in `api/roadmap.py` and rendered in the dashboard.

## Runtime Modes

| Mode | Meaning |
| --- | --- |
| `detection` | Fast object and feature extraction |
| `lab` | Adds morphology-oriented notes and geometry context |
| `semantic` | Scaffold for future compatibility and industrial-context reasoning |

## Inspection Scoring

`quality_score` is deterministic and bounded from `0.0` to `1.0`.

Inputs:

- detection state
- detection confidence
- wear score
- number of defect flags

Thresholds:

| Score | Result |
| --- | --- |
| `>= 0.72` | `PASS` |
| `>= 0.45` and `< 0.72` | `REVIEW` |
| `< 0.45` | `FAIL` |

## Detector Abstraction

Detector protocol:

```python
class Detector(Protocol):
    name: str
    model_name: str | None

    def detect(self, image, source: str, mode: RuntimeMode) -> DetectionResult:
        ...
```

Current detectors:

| Detector | Status |
| --- | --- |
| `OpenCVDetector` | Active deterministic fallback |
| `YoloDetector` | Adapter shell, inactive until model wiring exists |

## Telemetry Store

SQLite path:

```text
telemetry/screwvision.sqlite
```

The DB is local runtime state and ignored by git.
