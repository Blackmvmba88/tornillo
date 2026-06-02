from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from runtime.schemas import DetectionResult


class TelemetryStore:
    def __init__(self, db_path: Path = Path("telemetry/screwvision.sqlite")) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    source TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    detector TEXT NOT NULL DEFAULT 'unknown',
                    detected INTEGER NOT NULL,
                    family TEXT NOT NULL,
                    head_type TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    quality_score REAL NOT NULL DEFAULT 0.0,
                    inspection_result TEXT NOT NULL DEFAULT 'REVIEW',
                    payload TEXT NOT NULL
                )
                """
            )
            columns = {row[1] for row in conn.execute("PRAGMA table_info(detections)").fetchall()}
            if "detector" not in columns:
                conn.execute("ALTER TABLE detections ADD COLUMN detector TEXT NOT NULL DEFAULT 'unknown'")
            if "bbox" not in columns:
                conn.execute("ALTER TABLE detections ADD COLUMN bbox TEXT")
            if "quality_score" not in columns:
                conn.execute("ALTER TABLE detections ADD COLUMN quality_score REAL NOT NULL DEFAULT 0.0")
            if "inspection_result" not in columns:
                conn.execute("ALTER TABLE detections ADD COLUMN inspection_result TEXT NOT NULL DEFAULT 'REVIEW'")

    def record_detection(self, result: DetectionResult) -> None:
        payload = result.model_dump()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO detections (
                    source, mode, detector, detected, family, head_type, confidence,
                    quality_score, inspection_result, bbox, payload
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result.source,
                    result.mode,
                    result.detector,
                    int(result.detected),
                    result.classification.screw_family,
                    result.classification.head_type,
                    result.confidence,
                    result.quality_score,
                    result.inspection_result,
                    json.dumps(result.bbox.model_dump()) if result.bbox else None,
                    json.dumps(payload),
                ),
            )

    def summary(self) -> dict:
        with self._connect() as conn:
            total = conn.execute("SELECT COUNT(*) FROM detections").fetchone()[0]
            detected = conn.execute("SELECT COUNT(*) FROM detections WHERE detected = 1").fetchone()[0]
            avg_conf = conn.execute("SELECT AVG(confidence) FROM detections").fetchone()[0] or 0.0
            families = conn.execute(
                """
                SELECT family, COUNT(*) AS count
                FROM detections
                GROUP BY family
                ORDER BY count DESC
                LIMIT 10
                """
            ).fetchall()
            detectors = conn.execute(
                """
                SELECT detector, COUNT(*) AS count
                FROM detections
                GROUP BY detector
                ORDER BY count DESC
                LIMIT 10
                """
            ).fetchall()
            inspections = conn.execute(
                """
                SELECT inspection_result, COUNT(*) AS count
                FROM detections
                GROUP BY inspection_result
                ORDER BY count DESC
                """
            ).fetchall()

        return {
            "total_events": total,
            "detected_events": detected,
            "average_confidence": round(float(avg_conf), 3),
            "top_families": [{"family": row[0], "count": row[1]} for row in families],
            "detectors": [{"detector": row[0], "count": row[1]} for row in detectors],
            "inspection_results": [{"result": row[0], "count": row[1]} for row in inspections],
        }
