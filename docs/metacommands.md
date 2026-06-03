# ScrewVision Metacommands

This file documents the operating commands used to move ScrewVision forward without losing control of the repo.

Creator: **Iyari Cancino Gomez**, alias **BlackMamba**.

## Command Groups

| Intent | Command |
| --- | --- |
| Install Python runtime | `python3.11 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` |
| Install WebUI runtime | `cd webui && npm install` |
| Run Python tests | `.venv/bin/python -m pytest -q` |
| Build dashboard | `cd webui && npm run build` |
| Run API only | `.venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000` |
| Run WebUI only | `cd webui && npm run dev -- --host 0.0.0.0 --port 5173` |
| Run API + WebUI | `python3.11 scripts/dev.py` |
| Check API health | `curl http://127.0.0.1:8000/health` |
| Check roadmap API | `curl http://127.0.0.1:8000/roadmap` |
| Analyze one image from CLI | `.venv/bin/python runtime/main.py path/to/screw.jpg` |
| Analyze one image from API | `curl -X POST http://127.0.0.1:8000/detect -F image=@screw.jpg` |

## Release Metacommands

Use these when a PR has passed CI and is ready to become a public release.

```bash
gh pr ready <number>
gh pr merge <number> --squash --delete-branch

git checkout main
git pull --ff-only origin main

git tag vX.Y.Z
git push origin vX.Y.Z
```

The `v*` tag triggers `.github/workflows/release.yml`, which runs validation and publishes a release asset:

```text
screwvision-webui-vX.Y.Z.tar.gz
```

## Branch Metacommands

```bash
git checkout main
git pull --ff-only origin main
git checkout -b codex/<capability-name>
```

Recommended branch names:

```text
codex/mobile-camera-capture
codex/quality-inspection-layer
codex/go-to-market-kit
codex/multiclass-detection
```

## PR Validation Checklist

Before pushing a PR:

```bash
.venv/bin/python -m pytest -q
cd webui && npm run build
git diff --check
```

Before merging a PR:

```bash
gh pr view <number> --json state,isDraft,mergeable,statusCheckRollup
gh pr checks <number> --watch --interval 5
```

Expected checks:

```text
Python 3.11: pass
Python 3.12: pass
Web dashboard: pass
```

## Mobile Demo Metacommands

Run the local demo:

```bash
python3.11 scripts/dev.py
```

Open on the Mac:

```text
http://localhost:5173
```

Open on a phone on the same network:

```text
http://YOUR_MACHINE_IP:5173
```

The dashboard derives the API URL from the page host. A phone at `http://YOUR_MACHINE_IP:5173` calls `http://YOUR_MACHINE_IP:8000`.

Camera capture may be blocked by browser security when served over plain HTTP. If blocked, use upload fallback, run on the phone as `localhost`, or serve the dashboard over HTTPS.

## GitHub Auth Metacommand

Needed when changing workflows:

```bash
gh auth refresh -h github.com -s workflow
```

GitHub requires `workflow` scope to push `.github/workflows/*`.
