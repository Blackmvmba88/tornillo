from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from runtime.pipeline import ScrewVisionRuntime
from api.roadmap import ROADMAP, STACK_EVOLUTION
from telemetry.store import TelemetryStore

app = FastAPI(
    title="BlackMamba ScrewVision API",
    description="Mechanical intelligence runtime for screw recognition and analysis.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

runtime = ScrewVisionRuntime()
telemetry = TelemetryStore()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "runtime": "screwvision"}


@app.post("/detect")
async def detect(image: UploadFile = File(...)) -> dict:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upload must be an image.")

    payload = await image.read()
    result = runtime.analyze_image_bytes(payload, source=image.filename or "upload")
    telemetry.record_detection(result)
    return result.model_dump()


@app.get("/telemetry/summary")
def telemetry_summary() -> dict:
    return telemetry.summary()


@app.get("/roadmap")
def roadmap() -> dict:
    return {
        "vision": "Physics -> Vision -> Semantics -> Autonomy",
        "phases": ROADMAP,
        "stack_evolution": STACK_EVOLUTION,
    }
