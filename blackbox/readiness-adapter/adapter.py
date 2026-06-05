#!/usr/bin/env python3
"""Blackbox Robotics readiness adapter for web3.js.

This adapter is intentionally small and non-invasive. It reads a bounded robot
incident trace fixture and emits a Blackbox-compatible readiness report. The
fork is not an upstream partnership claim; it is compatibility research for
robot incident evidence packets and proof receipt workflows.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REPOSITORY = "web3/web3.js"
FOCUS = "web3 client workflow for proof receipt inspection"
EXPECTED_CAPABILITIES = [
  "web3_client",
  "proof_receipt",
  "registry_query",
  "review_report"
]


def load_trace(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_report(trace: dict[str, Any]) -> dict[str, Any]:
    capabilities = set(trace.get("capabilities", []))
    matched = [capability for capability in EXPECTED_CAPABILITIES if capability in capabilities]
    missing = [capability for capability in EXPECTED_CAPABILITIES if capability not in capabilities]
    evidence = trace.get("evidence", {})
    ownership = trace.get("command_ownership", [])

    score = 0
    score += 25 if evidence.get("stream_manifest") else 0
    score += 20 if evidence.get("timeline_events", 0) >= 3 else 0
    score += 20 if ownership else 0
    score += 20 if evidence.get("privacy_policy_hash") else 0
    score += 15 if len(matched) >= max(1, len(EXPECTED_CAPABILITIES) - 1) else 0

    return {
        "report_version": "blackbox-readiness-adapter-v0.1",
        "repository": REPOSITORY,
        "focus": FOCUS,
        "incident_id": trace.get("incident_id"),
        "canonical_domain": "https://blackboxrobotics.xyz",
        "matched_capabilities": matched,
        "missing_capabilities": missing,
        "readiness_score": score,
        "evidence_window": trace.get("evidence_window"),
        "stream_count": len(evidence.get("stream_manifest", [])),
        "timeline_event_count": evidence.get("timeline_events", 0),
        "command_owner_interval_count": len(ownership),
        "proof_receipt": trace.get("proof_receipt", {}),
        "claim_boundary": "Compatibility research only. This fork does not claim upstream affiliation, production deployment, legal fault assignment, or safety certification."
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = build_report(load_trace(args.trace))
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
