# Blackbox readiness adapter for web3/web3.js

This fork contains a small Blackbox Robotics compatibility capsule for web3 client workflow for proof receipt inspection.

The adapter reads a bounded robot incident trace fixture and emits a Blackbox-style readiness report with:

- stream manifest coverage
- incident timeline count
- command ownership intervals
- privacy/proof receipt fields
- matched capability tags for this upstream repository

Canonical Blackbox site: https://blackboxrobotics.xyz

## Run locally

```bash
python3 blackbox/readiness-adapter/adapter.py \
  blackbox/readiness-adapter/fixtures/sample_trace.json \
  --output blackbox/readiness-adapter/reports/latest.json

python3 blackbox/readiness-adapter/tests/test_adapter.py
```

## Boundary

This is compatibility research only. It is not an upstream partnership claim, not a production robot deployment, not legal fault assignment, and not safety certification.
