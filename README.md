# BlackMamba ScrewVision

![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![FastAPI](https://img.shields.io/badge/FastAPI-runtime-009688)
![OpenCV](https://img.shields.io/badge/OpenCV-vision-5C3EE8)

AI runtime for screw recognition, classification, geometry estimation, and industrial analysis.

This first implementation is intentionally runnable before a custom model exists:

- FastAPI detection API
- OpenCV morphology fallback analyzer
- Detector abstraction with bounding box response contract
- SQLite telemetry store
- CLI image analyzer
- React dashboard shell
- Tests for the runtime contracts

## Project Structure

```text
api/           FastAPI application
runtime/       Frame/image analysis runtime
ai/            Classifier and detector abstractions
telemetry/     SQLite event logging
webui/         React + Tailwind dashboard
docs/          Architecture and roadmap notes
scripts/       Local helper scripts
tests/         Python tests
models/        Model weights, ignored by git
datasets/      Training datasets, ignored by git
docker/        Deployment assets
```

## Quick Start

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn api.main:app --reload --port 8000
```

Analyze an image:

```bash
python runtime/main.py path/to/screw.jpg
```

Call the API:

```bash
curl -X POST http://localhost:8000/detect -F image=@screw.jpg
```

Run the dashboard:

```bash
cd webui
npm install
npm run dev
```

Run API and dashboard together:

```bash
python3.11 scripts/dev.py
```

## Runtime Modes

- `detection`: fast object and feature extraction
- `lab`: morphology metrics and contour-oriented analysis
- `semantic`: experimental compatibility and industrial-context layer

## Detection Contract

`POST /detect` returns a stable detector-neutral payload:

```json
{
  "detector": "opencv",
  "model": "contour-heuristic",
  "screw_type": "screw_or_bolt",
  "material": "bright_steel_or_aluminum",
  "wear": 0.12,
  "confidence": 0.71,
  "bbox": {
    "x": 10,
    "y": 20,
    "width": 140,
    "height": 24,
    "confidence": 0.71
  }
}
```

## Current AI Strategy

The repo ships with a deterministic OpenCV detector so the system is useful immediately. A YOLOv8 detector can be added under `ai/detectors.py` once trained weights and inference wiring are available in `models/`.

## Roadmap

The full product roadmap lives in [docs/roadmap.md](docs/roadmap.md) and is also exposed by the API:

```bash
curl http://localhost:8000/roadmap
```

Architecture evolution:

```text
PHASE 0 -> Object Detection
PHASE 1 -> Morphology
PHASE 2 -> Industrial Semantics
PHASE 3 -> Edge Intelligence
PHASE 4 -> Robotics
PHASE 5 -> Mechanical Cognition
PHASE 6 -> Cybernetic Factory Runtime
```

## License

MIT
