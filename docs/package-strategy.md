# Package Strategy

ScrewVision should be packaged as both a developer tool and an industrial runtime.

## Primary Packaging Targets

### 1. Docker Image

Best first target for factory demos and repeatable deployment.

```txt
ghcr.io/blackmvmba88/screwvision-api
```

Suggested runtime command:

```bash
docker run --rm -p 8000:8000 ghcr.io/blackmvmba88/screwvision-api:latest
```

Why Docker first:

- reproducible demo environment
- easier deployment on edge PCs
- avoids Python version conflicts
- works well with camera-station workflows

### 2. Python Package

Developer-facing package for runtime experiments.

```bash
pip install screwvision
```

Suggested package modules:

```txt
screwvision.runtime
screwvision.detectors
screwvision.telemetry
screwvision.api
screwvision.cli
```

### 3. Web Dashboard Build

Dashboard artifacts should be built and attached to releases.

```txt
screwvision-dashboard-vX.Y.Z.zip
```

## Release Assets

Each release should include practical artifacts, not only source archives.

Recommended release assets:

```txt
openapi.json
sample-inspection-report.json
sample-detection-output.png
docker-compose.yml
screwvision-dashboard.zip
```

## Versioning

Use semantic versioning:

```txt
v0.1.0  prototype runtime
v0.2.0  quality scoring
v0.3.0  mobile capture demo
v0.4.0  release automation
v0.5.0  factory inspection runtime
```

## Package Naming

Repository name can remain `tornillo`, but public product/package names should use:

```txt
ScrewVision
screwvision
screwvision-api
screwvision-dashboard
```

## Runtime Contract

Packages should preserve this stable inspection flow:

```txt
image input → detection → morphology → quality score → inspection result → telemetry
```

## Minimum Release Checklist

Before publishing a package or release:

- tests pass
- API starts locally
- dashboard starts locally
- `/detect` returns stable payload
- `/roadmap` works
- sample image produces a report
- release notes include breaking changes
- artifacts are attached

## Long-Term Distribution

Possible channels:

- GitHub Releases
- GitHub Container Registry
- PyPI
- Docker Compose bundle
- edge-device image

## Guiding Rule

Do not package vibes.

Package repeatable inspection behavior.
