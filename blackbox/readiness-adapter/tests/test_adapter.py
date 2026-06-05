import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapter.py"
FIXTURE = ROOT / "fixtures" / "sample_trace.json"

spec = importlib.util.spec_from_file_location("blackbox_readiness_adapter", ADAPTER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_build_report_has_blackbox_boundary():
    trace = json.loads(FIXTURE.read_text(encoding="utf-8"))
    report = module.build_report(trace)
    assert report["canonical_domain"] == "https://blackboxrobotics.xyz"
    assert report["readiness_score"] >= 85
    assert report["stream_count"] >= 3
    assert report["command_owner_interval_count"] >= 2
    assert "does not claim upstream affiliation" in report["claim_boundary"]


def test_cli_writes_report(tmp_path):
    output = tmp_path / "report.json"
    subprocess.run([sys.executable, str(ADAPTER), str(FIXTURE), "--output", str(output)], check=True)
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["report_version"] == "blackbox-readiness-adapter-v0.1"
    assert report["proof_receipt"]["status"] == "live_ready_not_broadcast"


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        test_build_report_has_blackbox_boundary()
        test_cli_writes_report(Path(tmp))
