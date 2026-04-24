#!/usr/bin/env python3
"""
StegDB Monitoring Hook — CI Status Emitter

Emits a structured status report that StegDB (or any downstream monitor)
can ingest to track repo health, trace validity, and ecosystem integration.

Usage (from CI):
    python stegdb_hooks/emit_status.py \
        --repo AaCT-E/demo \
        --run-id $GITHUB_RUN_ID \
        --sha $GITHUB_SHA \
        --status success \
        --traces-dir outputs/

Output: stegdb_hooks/last_status.json
"""

import argparse
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone


def hash_file(path: Path) -> str:
    """SHA-256 of file contents."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit StegDB-compatible status report")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--status", required=True, choices=["success", "failure", "cancelled"])
    parser.add_argument("--traces-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    traces_dir = args.traces_dir
    trace_files = sorted(traces_dir.glob("*_trace.json")) if traces_dir.exists() else []

    traces = []
    for tf in trace_files:
        data = json.loads(tf.read_text(encoding="utf-8"))
        traces.append({
            "scenario": data.get("scenario", tf.stem.replace("_trace", "")),
            "decision": data.get("decision"),
            "proposal_min_separation_nm": data.get("proposal_min_separation_nm"),
            "recovery_reachable": data.get("recovery_reachable"),
            "file": tf.name,
            "sha256_prefix": hash_file(tf),
        })

    report = {
        "schema_version": "1.0.0",
        "repo": args.repo,
        "run_id": args.run_id,
        "commit_sha": args.sha,
        "status": args.status,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "traces": traces,
        "ecosystem": {
            "org": "AaCT-E",
            "upstream": "GCAT-BCAT-Engine",
            "sibling_repos": [
                "GCAT-BCAT-Engine/Publisher",
                "StegVerse-Labs/StegDB",
                "StegVerse-Labs/SDK",
            ],
        },
    }

    out_path = Path("stegdb_hooks/last_status.json")
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"StegDB status emitted: {out_path}")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
