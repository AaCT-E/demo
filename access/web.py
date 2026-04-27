#!/usr/bin/env python3
"""
access/web.py — HTTP status endpoint for AaCT-E demo

Usage:
    python -m access.web --port 8080

Serves JSON status at GET /status using only stdlib http.server.
No external dependencies. Read-only observation endpoint.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, str(Path(__file__).parent.parent))

from access.cli import run_demo, verify


class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            results = run_demo()
            passed = verify(results)
            status = {
                "schema_version": "2.0.0",
                "repo": "AaCT-E/demo",
                "version": "0.2.0",
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "verification_passed": passed,
                "scenarios": results,
            }
            body = json.dumps(status, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "not found"}')

    def log_message(self, format, *args):
        # Suppress default logging
        pass


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), StatusHandler)
    print(f"AaCT-E status endpoint: http://{args.host}:{args.port}/status")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
