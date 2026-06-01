from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtime.pipeline import ScrewVisionRuntime
from telemetry.store import TelemetryStore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze screw imagery with ScrewVision.")
    parser.add_argument("image", type=Path, help="Path to an image file.")
    parser.add_argument(
        "--mode",
        choices=["detection", "lab", "semantic"],
        default="detection",
        help="Runtime analysis mode.",
    )
    parser.add_argument("--no-telemetry", action="store_true", help="Skip SQLite event logging.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    runtime = ScrewVisionRuntime(mode=args.mode)
    result = runtime.analyze_image_path(args.image)

    if not args.no_telemetry:
        TelemetryStore().record_detection(result)

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()
