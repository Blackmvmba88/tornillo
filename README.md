# BlackMamba ScrewVision

![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![FastAPI](https://img.shields.io/badge/FastAPI-runtime-009688)
![OpenCV](https://img.shields.io/badge/OpenCV-vision-5C3EE8)

ScrewVision is a lightweight industrial computer-vision runtime for screw recognition, morphology analysis, telemetry, and inspection workflows.

The project is intentionally runnable before custom model training exists. It uses deterministic OpenCV analysis today and keeps the detector contract ready for YOLO or future model backends.

## Creator

Created by **Iyari Cancino Gomez**, alias **BlackMamba**.

## Current Release

```text
Latest: v0.4.0
Focus: mobile capture + quality inspection scoring
```

Release line:

| Version | Capability |
| --- | --- |
| `v0.1.0` | Foundation runtime |
| `v0.2.0` | Visual detection layer and release automation |
| `v0.3.0` | Mobile camera capture demo |
| `v0.3.1` | Go-to-market documentation kit |
| `v0.4.0` | `quality_score` and `PASS` / `REVIEW` / `FAIL` inspection results |

## Product Surface

- FastAPI detection API
- OpenCV fallback detector
- Detector abstraction for future YOLO integration
- Bounding box response contract
- Quality inspection scoring
- SQLite telemetry store
- CLI image analyzer
- React/Vite dashboard
- Mobile camera capture and upload fallback
- CI for Python 3.11, Python 3.12, and WebUI build
- Automated GitHub releases with packaged WebUI assets

## Project Structure

```text
api/           FastAPI application and machine-readable roadmap
runtime/       Image analysis runtime and schemas
ai/            Detector protocol, OpenCV fallback, YOLO adapter shell
telemetry/     SQLite event logging
webui/         React + Tailwind dashboard
docs/          Architecture, roadmap, API, metacommands, and market notes
scripts/       Local helper scripts
tests/         Python contract tests
models/        Model weights, ignored by git
datasets/      Training datasets, ignored by git
docker/        Deployment assets
```

## Quick Start

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd webui
npm install
cd ..
```

Run checks:

```bash
.venv/bin/python -m pytest -q
cd webui && npm run build
```

Run API and dashboard together:

```bash
python3.11 scripts/dev.py
```

Open:

```text
http://localhost:5173
```

## Mobile Demo

Run the dev stack:

```bash
python3.11 scripts/dev.py
```

Open from a phone on the same network:

```text
http://YOUR_MACHINE_IP:5173
```

The dashboard derives the API URL from the page host, so a phone visiting `http://YOUR_MACHINE_IP:5173` calls `http://YOUR_MACHINE_IP:8000`.

Browser camera access usually requires HTTPS or `localhost`. If camera capture is blocked over plain HTTP, use upload fallback or serve the dashboard over HTTPS.

## API Commands

Health:

```bash
curl http://127.0.0.1:8000/health
```

Detect:

```bash
curl -X POST http://127.0.0.1:8000/detect -F image=@screw.jpg
```

Telemetry summary:

```bash
curl http://127.0.0.1:8000/telemetry/summary
```

Roadmap:

```bash
curl http://127.0.0.1:8000/roadmap
```

## Detection Contract

`POST /detect` returns a detector-neutral payload:

```json
{
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
  }
}
```

Inspection thresholds:

| Score | Result |
| --- | --- |
| `>= 0.72` | `PASS` |
| `>= 0.45` and `< 0.72` | `REVIEW` |
| `< 0.45` | `FAIL` |

## Documentation

| Document | Purpose |
| --- | --- |
| [docs/api-reference.md](docs/api-reference.md) | Endpoints, schemas, runtime modes, scoring, telemetry |
| [docs/metacommands.md](docs/metacommands.md) | Commands for development, PRs, releases, mobile demo, GitHub auth |
| [docs/architecture.md](docs/architecture.md) | Runtime architecture and integration points |
| [docs/roadmap.md](docs/roadmap.md) | Version history and future platform roadmap |
| [docs/go-to-market.md](docs/go-to-market.md) | Demo script, positioning, outreach copy, pricing anchors |

## Roadmap Summary

```text
v0.5.0 -> Multi-class industrial detection
v0.6.0 -> Dataset factory
v0.7.0 -> Calibration and measurement
v1.0.0 -> Mechanical Intelligence Platform
```

The machine-readable roadmap lives in `api/roadmap.py` and is exposed at `GET /roadmap`.

## License

MIT
