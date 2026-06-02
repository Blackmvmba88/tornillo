from __future__ import annotations

import signal
import socket
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_PORT = 8000
WEB_PORT = 5173
DEV_HOST = "0.0.0.0"


def port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.25)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def wait_for_port(name: str, port: int, timeout: float = 12.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if port_open(port):
            print(f"[ok] {name} listening on {port}", flush=True)
            return True
        time.sleep(0.25)
    print(f"[warn] {name} did not open port {port} within {timeout:.0f}s", flush=True)
    return False


def start_process(name: str, command: list[str], cwd: Path) -> subprocess.Popen:
    print(f"[start] {name}: {' '.join(command)}", flush=True)
    return subprocess.Popen(command, cwd=cwd)


def main() -> int:
    api_python = ROOT / ".venv" / "bin" / "python"
    if not api_python.exists():
        print("[error] Missing .venv. Run: python3.11 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt", flush=True)
        return 1

    processes = [
        start_process(
            "api",
            [str(api_python), "-m", "uvicorn", "api.main:app", "--host", DEV_HOST, "--port", str(API_PORT)],
            ROOT,
        ),
        start_process(
            "webui",
            ["npm", "run", "dev", "--", "--host", DEV_HOST, "--port", str(WEB_PORT)],
            ROOT / "webui",
        ),
    ]

    def stop(_signum: int | None = None, _frame: object | None = None) -> None:
        print("\n[stop] shutting down ScrewVision dev runtime", flush=True)
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    wait_for_port("api", API_PORT)
    wait_for_port("webui", WEB_PORT)

    print("\nScrewVision dev runtime", flush=True)
    print(f"  API:       http://127.0.0.1:{API_PORT}", flush=True)
    print(f"  Dashboard: http://localhost:{WEB_PORT}", flush=True)
    print("  Network:   use your machine IP on the same ports", flush=True)
    print("  Stop:      Ctrl+C\n", flush=True)

    try:
        while all(process.poll() is None for process in processes):
            time.sleep(0.5)
    finally:
        stop()

    failed = [process.returncode for process in processes if process.returncode not in (0, None, -15)]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
