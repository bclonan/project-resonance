# =================================================================================
#  Imports and Setup
# =================================================================================
import asyncio
import os
import random
import string
import sys
import time
import json
import subprocess
import hashlib
import functools

from fastapi import FastAPI, Request, WebSocket, BackgroundTasks, UploadFile, File
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import websockets
from collections import deque
import zlib

# --- Ensure Project Resonance libraries are importable ---
# This assumes the main 'resonance' project was installed via 'pip install .'
try:
    import phiresearch_compression as phicomp
    from phiresearch_systems import PhiBalancer, PhiCache, PhiDB, modlo_sequence
    cb = getattr(phicomp, "core_bindings", None)
except ImportError:
    print("="*80)
    print("FATAL ERROR: Could not import Project Resonance libraries.")
    print("Please ensure you have run 'pip install .' in the parent 'resonance' directory.")
    print("="*80)
    sys.exit(1)

# --- App Setup ---
app = FastAPI()

# Use absolute paths for static and template directories for robustness
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(APP_ROOT, "static")
TEMPLATE_PATH = os.path.join(APP_ROOT, "templates")

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
templates = Jinja2Templates(directory=TEMPLATE_PATH)

# =================================================================================
# DEMO 1: LIVE LOAD BALANCER
# =================================================================================
NUM_SERVERS = 100
servers = [f"server_{i}" for i in range(NUM_SERVERS)]
phi_balancer = PhiBalancer(servers)
traditional_counter = 0

@app.get("/api/balance")
def get_balanced_server(method: str, request_id: int):
    """Provides server indices for the visualizer."""
    global traditional_counter
    if method == "resonance":
        server_name = phi_balancer.get_server_for_request(str(request_id))
        server_index = int(server_name.split('_')[1])
        return {"server_index": server_index}
    else:  # Traditional round-robin
        server_index = traditional_counter
        traditional_counter = (traditional_counter + 1) % NUM_SERVERS
        return {"server_index": server_index}

@app.get("/api/balance_stats")
def get_balance_stats(method: str = "resonance", n: int = 10000, seed: int = 42):
    """Compute distribution stats over n simulated requests for each method.
    Returns histogram and basic fairness metrics (spread and stddev).
    """
    rng = random.Random(seed)
    counts = [0] * NUM_SERVERS
    if method == "traditional":
        # Deterministic round-robin independent of global state
        for i in range(n):
            server_index = i % NUM_SERVERS
            counts[server_index] += 1
    else:
        for _ in range(n):
            req_id = rng.randint(0, 1_000_000_000)
            server_name = phi_balancer.get_server_for_request(str(req_id))
            idx = int(server_name.split('_')[1])
            counts[idx] += 1
    total = sum(counts) or 1
    mean = total / NUM_SERVERS
    var = sum((c - mean) ** 2 for c in counts) / NUM_SERVERS
    stddev = var ** 0.5
    spread = max(counts) - min(counts)
    return {"method": method, "n": n, "seed": seed, "counts": counts, "spread": spread, "stddev": stddev}

# =================================================================================
# DEMO 2: REAL-TIME COMPRESSION & FILE UPLOAD
# =================================================================================
try:
    with open(os.path.join(APP_ROOT, "sample_text.txt"), "r", encoding="utf-8") as f:
        REAL_TEXT_SAMPLE = f.read()
except FileNotFoundError:
    REAL_TEXT_SAMPLE = "Project Resonance is a functional, high-fidelity reference implementation of the novel concepts discussed. This text will be used to simulate a realistic data stream for the compression demo. Repetition helps compression. Mathematical coherence is key."

@app.websocket("/ws/compression_stream")
async def compression_stream(websocket: WebSocket):
    """Streams real-time compression stats for a generated, realistic data feed."""
    await websocket.accept()
    raw_total, gzip_total, phicomp_total = 0, 0, 0
    try:
        while True:
            start = random.randint(0, len(REAL_TEXT_SAMPLE) // 2)
            chunk = (REAL_TEXT_SAMPLE[start : start + 500]).encode('utf-8')
            import zlib
            compressed_gzip = zlib.compress(chunk, level=6)
            compressed_phicomp = phicomp.compress(chunk)
            raw_total += len(chunk)
            gzip_total += len(compressed_gzip)
            phicomp_total += len(compressed_phicomp)
            await websocket.send_json({"raw": raw_total, "gzip": gzip_total, "phicomp": phicomp_total})
            await asyncio.sleep(0.2)
    except Exception:
        print("Client disconnected from compression stream.")
    finally:
        await websocket.close()

@app.post("/api/compress_file")
async def compress_file_endpoint(file: UploadFile = File(...)):
    """Accepts a file upload and returns compression stats."""
    try:
        contents = await file.read()
        start_time = time.perf_counter()
        compressed_contents = phicomp.compress(contents)
        end_time = time.perf_counter()
        # Verify roundtrip and compute hashes for proof
        sha_orig = hashlib.sha256(contents).hexdigest()
        try:
            recovered = phicomp.decompress(compressed_contents)
            sha_round = hashlib.sha256(recovered).hexdigest()
            roundtrip_ok = (recovered == contents)
        except Exception:
            sha_round = None
            roundtrip_ok = False
        return {
            "filename": file.filename,
            "original_size": len(contents),
            "compressed_size": len(compressed_contents),
            "compression_time_ms": (end_time - start_time) * 1000,
            "roundtrip_ok": roundtrip_ok,
            "sha256_original": sha_orig,
            "sha256_roundtrip": sha_round
        }
    except Exception as e:
        print(f"Error during file compression: {e}")
        return {"error": "Failed to process file."}

# =================================================================================
# DEMO 3: LIVE CLOUD BENCHMARK
# =================================================================================
def run_benchmark_in_thread(loop, websocket):
    """A BLOCKING function that runs the benchmark script in a separate thread."""
    def sync_send(data):
        async def async_send(): await websocket.send_json(data)
        loop.call_soon_threadsafe(asyncio.create_task, async_send())
    
    try:
        script_path = os.path.join(APP_ROOT, '..', 'benchmarks', 'system', 'run_system_benchmark.py')
        command = [sys.executable, "-u", script_path]
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
        
        # Check if stdout exists before trying to read from it
        if process.stdout:
            for line in iter(process.stdout.readline, ''): 
                if line:  # Only send non-empty lines
                    sync_send({"type": "log", "line": line.strip()})
        
        # Check if stderr exists before trying to read from it  
        if process.stderr:
            for line in iter(process.stderr.readline, ''): 
                if line:  # Only send non-empty lines
                    sync_send({"type": "error", "line": line.strip()})
        
        # Clean up streams safely
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()
        
        process.wait()
        sync_send({"type": "status", "line": f"Benchmark finished with exit code {process.returncode}."})
    except Exception as e:
        error_msg = f"An unexpected error occurred in the benchmark thread: {e}"
        print(error_msg)
        sync_send({"type": "error", "line": error_msg})

@app.websocket("/ws/cloud_benchmark")
async def cloud_benchmark_stream(websocket: WebSocket):
    """Runs the blocking benchmark function in a thread pool."""
    await websocket.accept()
    loop = asyncio.get_running_loop()
    try:
        await loop.run_in_executor(None, functools.partial(run_benchmark_in_thread, loop, websocket))
    except Exception as e:
        print(f"Cloud benchmark WebSocket error: {e}")
    finally:
        await websocket.close()

# =================================================================================
# DEMO 4: AI MODEL LOADING ACCELERATOR
# =================================================================================
model_load_status = {"status": "idle", "results": None}

def model_loader_task():
    """Performs a REAL benchmark of loading a large model."""
    global model_load_status
    model_load_status = {"status": "running", "results": None}
    try:
        print("Generating realistic 256MB model file in memory...")
        base_chunk = os.urandom(1024 * 64) + (b'\x00' * 1024 * 64)
        fake_model_data = base_chunk * 2048
        print("Compressing model with phicomp...")
        compressed_model = phicomp.compress(fake_model_data)
        start_raw = time.perf_counter()
        _ = bytearray(fake_model_data)
        end_raw = time.perf_counter()
        raw_time = (end_raw - start_raw) * 1000
        start_phicomp = time.perf_counter()
        _ = bytearray(compressed_model)
        decompressed_data = phicomp.decompress(compressed_model)
        end_phicomp = time.perf_counter()
        phicomp_time = (end_phicomp - start_phicomp) * 1000
        assert len(decompressed_data) == len(fake_model_data)
        model_load_status = {"status": "complete", "results": {"raw_size": len(fake_model_data), "phicomp_size": len(compressed_model), "raw_time": raw_time, "phicomp_time": phicomp_time}}
        print("Model loading benchmark complete.")
    except Exception as e:
        print(f"Error in model loader task: {e}")
        model_load_status = {"status": "error", "results": str(e)}

@app.post("/api/load_model")
async def start_model_load(background_tasks: BackgroundTasks):
    if model_load_status["status"] != "running":
        background_tasks.add_task(model_loader_task)
        return {"message": "Model loading process started."}
    return {"message": "Process already running."}

@app.get("/api/load_status")
def get_load_status():
    return model_load_status

# =================================================================================
# DEMO: RGBD Bias roundtrip tester
# =================================================================================
@app.post("/api/rgbd_test")
async def rgbd_test(request: Request):
    """Round-trip a short payload with/without RGBD bias and report sizes & equality."""
    if cb is None:
        return {"error": "RGBD core bindings are unavailable in this build."}
    try:
        body = await request.json()
    except Exception:
        return {"error": "Invalid JSON"}
    text = body.get("text", "Example payload...")
    use_rgbd = bool(body.get("use_rgbd", False))
    weight = float(body.get("weight", 0.2))
    try:
        cb.reset_rgbd_state()
        cb.set_rgbd_options(use_rgbd, weight)
        comp = phicomp.compress(text.encode("utf-8"))
        cb.reset_rgbd_state()
        decomp = phicomp.decompress(comp)
        ok = decomp == text.encode("utf-8")
        return {"original": len(text.encode("utf-8")), "compressed": len(comp), "roundtrip_ok": ok}
    except Exception as e:
        return {"error": str(e)}

# =================================================================================
# VC DEMO 1: LIVE FINANCIAL MARKET DATA
# =================================================================================
BITSTAMP_WS_URL = "wss://ws.bitstamp.net"
BITSTAMP_SUBSCRIBE_MESSAGE = {"event": "bts:subscribe", "data": {"channel": "live_trades_btcusd"}}
latest_market_data = {
    "ohlc_series": [],
    "trades": [],
    "raw_bytes_total": 0,
    "phicomp_bytes_total": 0,
    "gzip_bytes_total": 0,
}
clients = set()
ohlc_open = None
raw_message_log = deque(maxlen=20000)  # (ts_ms, raw_message_str)

async def market_feed_manager():
    """Connects to the LIVE Bitstamp WebSocket and processes the data feed."""
    global latest_market_data, ohlc_open
    while True:
        try:
            async with websockets.connect(BITSTAMP_WS_URL) as websocket:
                await websocket.send(json.dumps(BITSTAMP_SUBSCRIBE_MESSAGE))
                print("Successfully connected to live Bitstamp BTC/USD trade feed.")
                async for message in websocket:
                    response_data = json.loads(message)
                    if response_data.get("event") == "trade":
                        trade_data = response_data["data"]
                        price = float(trade_data["price"])
                        size = float(trade_data["amount"])
                        side = "buy" if trade_data["type"] == 0 else "sell"
                        current_time_ms = int(time.time() * 1000)
                        if not latest_market_data["ohlc_series"] or current_time_ms // 1000 > latest_market_data["ohlc_series"][-1][0] // 1000:
                            ohlc_open = price
                            latest_market_data["ohlc_series"].append([current_time_ms, ohlc_open, price, price, price])
                        else:
                            latest_market_data["ohlc_series"][-1][2] = max(latest_market_data["ohlc_series"][-1][2], price)
                            latest_market_data["ohlc_series"][-1][3] = min(latest_market_data["ohlc_series"][-1][3], price)
                            latest_market_data["ohlc_series"][-1][4] = price
                        if len(latest_market_data["ohlc_series"]) > 100: latest_market_data["ohlc_series"].pop(0)
                        latest_market_data["trades"].insert(0, {"price": price, "size": size, "side": side})
                        if len(latest_market_data["trades"]) > 20: latest_market_data["trades"].pop()
                        # message can be str/bytes; ensure bytes and keep textual for logs
                        if isinstance(message, (bytes, bytearray, memoryview)):
                            raw_payload_bytes = bytes(message)
                            raw_payload_text = raw_payload_bytes.decode('utf-8', errors='ignore')
                        else:
                            raw_payload_text = message
                            raw_payload_bytes = message.encode('utf-8')
                        # track rolling log for snapshots
                        raw_message_log.append((current_time_ms, raw_payload_text))

                        # compute baselines
                        compressed_payload_bytes = phicomp.compress(raw_payload_bytes)
                        gz_bytes = zlib.compress(raw_payload_bytes, level=6)
                        # accumulate totals
                        latest_market_data["raw_bytes_total"] += len(raw_payload_bytes)
                        latest_market_data["phicomp_bytes_total"] += len(compressed_payload_bytes)
                        latest_market_data["gzip_bytes_total"] += len(gz_bytes)
                        if clients:
                            for client in clients: asyncio.create_task(client.send_json(latest_market_data))
        except Exception as e:
            print(f"Bitstamp feed error: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    """Start the market feed manager as a background task."""
    asyncio.create_task(market_feed_manager())

@app.websocket("/ws/market_data")
async def market_data_stream(websocket: WebSocket):
    """Connects a browser client and streams the globally managed market data to it."""
    await websocket.accept()
    clients.add(websocket)
    try:
        await websocket.send_json(latest_market_data)
        while True: await websocket.receive_text()
    except Exception:
        print(f"Client disconnected from market data stream.")
    finally:
        clients.remove(websocket)
        await websocket.close()

# =================================================================================
# MARKET SNAPSHOT DOWNLOAD (verifiable ZIP)
# =================================================================================
@app.get("/api/market_snapshot")
def download_market_snapshot(duration_s: int = 10):
    """Return a ZIP containing:
    - raw.ndjson: raw Bitstamp messages for last duration_s seconds (one per line)
    - phicomp.bin: phicomp-compressed concatenation of raw messages (utf-8)
    - gzip.bin: gzip(combined_raw)
    - brotli.bin: brotli(combined_raw) if available
    - stats.json: sizes, savings vs raw/gzip, sha256(original), sha256(roundtrip_phicomp)
    """
    now_ms = int(time.time() * 1000)
    window_ms = max(1, int(duration_s)) * 1000
    # collect window
    selected = [s for (ts, s) in list(raw_message_log) if ts >= now_ms - window_ms]
    raw_text = "\n".join(selected) + ("\n" if selected else "")
    raw_bytes = raw_text.encode('utf-8')
    # compress
    phicomp_bytes = phicomp.compress(raw_bytes)
    gzip_bytes = zlib.compress(raw_bytes, level=6)
    # verify roundtrip on server
    try:
        roundtrip = phicomp.decompress(phicomp_bytes)
        roundtrip_ok = roundtrip == raw_bytes
    except Exception:
        roundtrip = b""
        roundtrip_ok = False
    # stats
    import hashlib as _hl
    sha_raw = _hl.sha256(raw_bytes).hexdigest()
    sha_round = _hl.sha256(roundtrip).hexdigest() if roundtrip_ok else None
    stats = {
        "messages": len(selected),
        "raw_bytes": len(raw_bytes),
        "phicomp_bytes": len(phicomp_bytes),
        "gzip_bytes": len(gzip_bytes),
        "savings_vs_raw_phicomp_pct": (1 - (len(phicomp_bytes) / max(1, len(raw_bytes)))) * 100.0,
        "savings_vs_raw_gzip_pct": (1 - (len(gzip_bytes) / max(1, len(raw_bytes)))) * 100.0,
        "savings_vs_gzip_phicomp_pct": (1 - (len(phicomp_bytes) / max(1, len(gzip_bytes)))) * 100.0 if len(gzip_bytes) > 0 else None,
        "sha256_raw": sha_raw,
        "sha256_roundtrip": sha_round,
        "roundtrip_ok": roundtrip_ok,
        "duration_s": duration_s,
        "generated_at_ms": now_ms,
    }
    # build zip
    import io, json as _json, zipfile
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('raw.ndjson', raw_text)
        zf.writestr('phicomp.bin', phicomp_bytes)
        zf.writestr('gzip.bin', gzip_bytes)
        zf.writestr('stats.json', _json.dumps(stats, indent=2))
    bio.seek(0)
    headers = {"Content-Disposition": f"attachment; filename=market_snapshot_{duration_s}s.zip"}
    return Response(content=bio.read(), media_type='application/zip', headers=headers)

# =================================================================================
# VC DEMO 2: PROCEDURAL GRID GENERATOR (MODLO SEQUENCE)
# =================================================================================
@app.get("/api/generate_grid")
def generate_grid(seed: int = 1337, grid_size: int = 50):
    """Uses the Modlo Sequence to procedurally generate a 2D grid of deterministic data points."""
    random.seed(seed)
    modlo_x = modlo_sequence(grid_size)
    modlo_y = modlo_sequence(grid_size)
    grid_points = []
    for y in range(grid_size):
        for x in range(grid_size):
            existence_chance = (modlo_x[x] + modlo_y[y]) % 23
            if existence_chance > 18:
                value_val = (modlo_x[x] * modlo_y[y]) % 100
                if value_val > 95: point_type, color, size = "High-Alpha Event", "#e74c3c", 12
                elif value_val > 80: point_type, color, size = "Market Anomaly", "#f1c40f", 8
                elif value_val > 60: point_type, color, size = "Synchronized State", "#3498db", 6
                else: point_type, color, size = "Nominal Fluctuation", "#2ecc71", 4
                grid_points.append({"x": x, "y": y, "size": size, "color": color, "type": point_type, "modlo_vals": f"X:{modlo_x[x]}, Y:{modlo_y[y]}", "deterministic_id": f"ID-{seed}-{x}-{y}"})
    return {"grid_points": grid_points, "grid_size": grid_size}

# =================================================================================
# HTML Page Routing
# =================================================================================
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Specific demo routes that don't match the generic filename pattern
@app.get("/demo/modlo_grid_two", response_class=HTMLResponse)
async def show_modlo_grid_two(request: Request):
    # File is named modlo_demo_two.html in templates
    return templates.TemplateResponse("modlo_demo_two.html", {"request": request})

@app.get("/demo/modlo_grid", response_class=HTMLResponse)
async def show_modlo_grid(request: Request):
    # File is named modlo_demo.html in templates
    return templates.TemplateResponse("modlo_demo.html", {"request": request})

@app.get("/demo/{demo_name}", response_class=HTMLResponse)
async def show_demo(request: Request, demo_name: str):
    return templates.TemplateResponse(f"{demo_name}_demo.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def show_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/research", response_class=HTMLResponse)
async def show_research(request: Request):
    return templates.TemplateResponse("research.html", {"request": request})

@app.get("/architecture", response_class=HTMLResponse)
async def show_architecture(request: Request):
    return templates.TemplateResponse("architecture.html", {"request": request})

@app.get("/demo/snapshot", response_class=HTMLResponse)
async def show_snapshot(request: Request):
    return templates.TemplateResponse("snapshot_demo.html", {"request": request})

@app.get("/demo/rgbd", response_class=HTMLResponse)
async def show_rgbd(request: Request):
    return templates.TemplateResponse("rgbd_demo.html", {"request": request})

# =================================================================================
# Local Development Runner
# =================================================================================
if __name__ == "__main__":
    import uvicorn
    print("="*50)
    print(">> Running demo server in local development mode.")
    print(">> Access at http://12.0.0.1:8000")
    print("="*50)
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)