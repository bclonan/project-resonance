# Resonance Demos

This folder contains real-world demos showcasing the core components of Project Resonance: compression (phicomp), balanced request routing, cloud/system benchmarking, and live visualizations.

## Quick start

- Install from repo root:

```bash
pip install .
```

- Install demo deps, then run the demo app:

```bash
cd resonance_demos
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open <http://127.0.0.1:8000> in your browser.

## What’s included

- Compression demo: Upload a file or stream payloads and see size deltas and latency.
- Cloud/system benchmark: Spawn the included benchmark runner and stream updates live.
- Market data demo: Live BTC/USD feed with OHLC charts; tracks raw vs phicomp-compressed byte totals.
- Modlo grid demo: Procedural grid generator to visualize sequence dynamics.

### Verify bold claims hands-on (Modlo demo)

Under the Modlo grid demo, we include quick actions for self-verification:

- Export grid as JSON: Builds a world layout from the seed and downloads a tiny JSON file. Share only the seed; others can reproduce the same world.
- Compute fingerprint: Produces a short, deterministic code for the current seed/world. Two people with the same seed should see the same code.
- Generate deterministic price series (CSV): Creates a reproducible HFT-like time series from the seed. Great for backtesting consistency.
- Generate 1000 sensor states (JSON): Outputs a deterministic snapshot for a digital twin simulation. Share the seed to sync states across teams.

## Real-world usage examples

- API payload compression:

```python
import json
import phiresearch_compression as phicomp

payload = {"user_id": 42, "items": list(range(1000))}
raw = json.dumps(payload).encode()
compressed = phicomp.compress(raw)
# send compressed over wire, or store

recovered = phicomp.decompress(compressed)
assert recovered == raw
```

- Streaming compression snapshot (WebSocket handler skeleton):

```python
from fastapi import WebSocket
import phiresearch_compression as phicomp

async def stream(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            msg = await ws.receive_text()
            b = msg.encode()
            cb = phicomp.compress(b)
            await ws.send_json({"in": len(b), "out": len(cb)})
    finally:
        await ws.close()
```

- Batch log compaction:

```python
from pathlib import Path
import phiresearch_compression as phicomp

logs = b"".join(p.read_bytes() for p in Path("/var/log/myapp").glob("*.log"))
blob = phicomp.compress(logs)
Path("/var/archive/logs.bin").write_bytes(blob)
```

## Notes

- Windows users need MSVC Build Tools.
- For serverless hosting (Netlify), see repo root README and `netlify/functions/`.
- Experimental RGBD bias can be toggled via `phiresearch_compression.core_bindings.set_rgbd_options(use_rgbd, weight)`.

Tip: If a teammate gets a different result, confirm you’re using the exact same seed string (case and whitespace matter). Then click Compute fingerprint — it must match on both sides.
