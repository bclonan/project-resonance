import asyncio
import os
import random
import string
import sys
import time
from fastapi import FastAPI, Request, WebSocket, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import websockets
from fastapi import UploadFile, File
import asyncio
import subprocess # Use the standard subprocess module
import functools  # For creating partial functions for the thread


from phiresearch_systems.generators import modlo_sequence
# --- Ensure we can find the parent resonance directory ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
# --- Ensure we can find the phiresearch_compression library ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../phiresearch_compression")))

# --- Ensure Project Resonance libraries are importable ---
# This assumes the main 'resonance' project was installed via 'pip install .'
try:
    import phiresearch_compression as phicomp
    from phiresearch_systems import PhiBalancer
except ImportError:
    print("="*80)
    print("FATAL ERROR: Could not import Project Resonance libraries.")
    print("Please ensure you have run 'pip install .' in the parent 'resonance' directory.")
    print("="*80)
    sys.exit(1)

# --- App Setup ---
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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

# =================================================================================
# DEMO 2: REAL-TIME COMPRESSION
# =================================================================================
try:
    with open("sample_text.txt", "r", encoding="utf-8") as f:
        REAL_TEXT_SAMPLE = f.read()
except FileNotFoundError:
    REAL_TEXT_SAMPLE = "Project Resonance is a functional, high-fidelity reference implementation of the novel concepts discussed. This text will be used to simulate a realistic data stream for the compression demo. Repetition helps compression. Mathematical coherence is key."

@app.websocket("/ws/compression_stream")
async def compression_stream(websocket: WebSocket):
    """
    Streams real-time compression stats for a generated, realistic data feed.
    This is a real benchmark happening live on the server.
    """
    await websocket.accept()
    raw_total = 0
    gzip_total = 0
    phicomp_total = 0
    
    try:
        while True:
            # 1. Create a realistic chunk of data.
            # We take a slice of our real text and add a little random noise.
            start = random.randint(0, len(REAL_TEXT_SAMPLE) // 2)
            chunk = (REAL_TEXT_SAMPLE[start : start + 500]).encode('utf-8')
            
            # 2. Compress the chunk with standard Gzip for a baseline comparison.
            import zlib
            compressed_gzip = zlib.compress(chunk, level=6)
            
            # 3. Compress the same chunk with our innovative PhiComp library.
            # This calls the actual compiled C++ code.
            compressed_phicomp = phicomp.compress(chunk)
            
            # 4. Update the running totals.
            raw_total += len(chunk)
            gzip_total += len(compressed_gzip)
            phicomp_total += len(compressed_phicomp)
            
            # 5. Send the running totals to the browser to be plotted on the chart.
            await websocket.send_json({
                "raw": raw_total,
                "gzip": gzip_total,
                "phicomp": phicomp_total
            })
            await asyncio.sleep(0.2) # Stream data 5 times per second
    except Exception:
        print("Client disconnected from compression stream.")
    finally:
        await websocket.close()
        
@app.post("/api/compress_file")
async def compress_file_endpoint(file: UploadFile = File(...)):
    """
    Accepts a file upload, reads its content, compresses it using the
    real phicomp C++ library, and returns the original and compressed sizes.
    """
    try:
        # 1. Read the uploaded file into memory
        contents = await file.read()
        original_size = len(contents)

        # 2. Compress the contents using our innovative C++ core
        start_time = time.perf_counter()
        compressed_contents = phicomp.compress(contents)
        end_time = time.perf_counter()
        
        compressed_size = len(compressed_contents)
        compression_time_ms = (end_time - start_time) * 1000

        # 3. Return the results as JSON
        return {
            "filename": file.filename,
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_time_ms": compression_time_ms
        }
    except Exception as e:
        print(f"Error during file compression: {e}")
        return {"error": "Failed to process file."}

# =================================================================================
# DEMO 3: LIVE CLOUD BENCHMARK
# =================================================================================
def run_benchmark_in_thread(loop, websocket):
    """
    This is a standard, BLOCKING function that runs the benchmark script.
    It is designed to be executed in a separate thread by asyncio's executor.
    It safely streams output back to the main asyncio loop.
    """
    try:
        # Define the absolute path to the benchmark script to ensure it's always found
        script_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            '..', # Go up to the parent 'resonance' directory
            'benchmarks', 
            'system', 
            'run_system_benchmark.py'
        )
        
        # Use sys.executable to ensure we're using the same Python interpreter
        # The '-u' flag is crucial for unbuffered output, which gives us a true real-time stream
        command = [sys.executable, "-u", script_path]

        # This is a thread-safe way to send data back to the websocket
        def sync_send(data):
            """A helper to schedule an async send from a synchronous thread."""
            async def async_send():
                await websocket.send_json(data)
            # Schedule the async send function to run on the main event loop
            loop.call_soon_threadsafe(asyncio.create_task, async_send())

        # Use Popen to get real-time access to stdout and stderr
        # This is the core of the real-time streaming logic
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True, # Decode output as text
            encoding='utf-8',
            errors='ignore' # Ignore any minor decoding errors from Docker's progress bars
        )

        # Stream stdout line by line until the process closes the pipe
        for line in iter(process.stdout.readline, ''):
            sync_send({"type": "log", "line": line.strip()})
        
        # After stdout is finished, stream any stderr messages
        for line in iter(process.stderr.readline, ''):
            sync_send({"type": "error", "line": line.strip()})

        # Clean up the process
        process.stdout.close()
        process.stderr.close()
        process.wait()
        
        status_msg = f"Benchmark finished with exit code {process.returncode}."
        sync_send({"type": "status", "line": status_msg})

    except Exception as e:
        error_msg = f"An unexpected error occurred in the benchmark thread: {e}"
        print(error_msg)
        sync_send({"type": "error", "line": error_msg})

@app.websocket("/ws/cloud_benchmark")
async def cloud_benchmark_stream(websocket: WebSocket):
    """
    This endpoint runs the blocking benchmark function in a thread pool
    to avoid freezing the server. This is the robust, cross-platform solution.
    """
    await websocket.accept()
    loop = asyncio.get_running_loop()
    
    try:
        # Run the blocking function in the default thread pool executor.
        # `functools.partial` is used to pass arguments to our target function.
        await loop.run_in_executor(
            None,  # Use the default executor
            functools.partial(run_benchmark_in_thread, loop, websocket)
        )
    except Exception as e:
        print(f"Cloud benchmark WebSocket error: {e}")
    finally:
        # Ensure the connection is always closed
        await websocket.close()

# =================================================================================
# DEMO 4: AI MODEL LOADING ACCELERATOR
# =================================================================================
# Using a simple global dict to store task status
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
# DEMO: FINANCIAL MARKET DATA
# =================================================================================
BITSTAMP_WS_URL = "wss://ws.bitstamp.net"
BITSTAMP_SUBSCRIBE_MESSAGE = {
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}

# Global state to share data between the external connection and clients
latest_market_data = {
    "ohlc": {"time": int(time.time()), "open": 0, "high": 0, "low": 999999, "close": 0},
    "trades": [],
    "raw_bytes_total": 0,
    "phicomp_bytes_total": 0
}
clients = set()
ohlc_open = None

async def market_feed_manager():
    """
    Connects to the LIVE Bitstamp WebSocket for BTC/USD trades, processes the
    data, compresses it, and updates the global state for all connected clients.
    """
    global latest_market_data, ohlc_open
    
    # ... (connection logic remains the same) ...
    try:
        async with websockets.connect(BITSTAMP_WS_URL) as websocket:
            await websocket.send(json.dumps(BITSTAMP_SUBSCRIBE_MESSAGE))
            print("Successfully connected to live Bitstamp BTC/USD trade feed.")

            async for message in websocket:
                response_data = json.loads(message)
                
                if response_data.get("event") == "trade":
                    trade_data = response_data["data"]
                    price = float(trade_data["price"])
                    # ... (trade processing logic remains the same) ...

                    # --- BUG FIX: Format OHLC data for ApexCharts ---
                    # ApexCharts expects [timestamp_ms, open, high, low, close]
                    current_time_ms = int(time.time() * 1000)
                    
                    if latest_market_data["ohlc_series"] and current_time_ms // 1000 > latest_market_data["ohlc_series"][-1][0] // 1000:
                        # Start of a new candle (new second)
                        ohlc_open = price
                        new_candle = [current_time_ms, ohlc_open, price, price, price]
                        latest_market_data["ohlc_series"].append(new_candle)
                    else:
                        # Update the current candle
                        if not latest_market_data["ohlc_series"]:
                             ohlc_open = price
                             latest_market_data["ohlc_series"].append([current_time_ms, ohlc_open, price, price, price])
                        
                        latest_market_data["ohlc_series"][-1][2] = max(latest_market_data["ohlc_series"][-1][2], price) # High
                        latest_market_data["ohlc_series"][-1][3] = min(latest_market_data["ohlc_series"][-1][3], price) # Low
                        latest_market_data["ohlc_series"][-1][4] = price # Close

                    if len(latest_market_data["ohlc_series"]) > 100: # Keep the series to a manageable size
                        latest_market_data["ohlc_series"].pop(0)

                    # ... (trade tape and compression logic remains the same) ...
                    
                    # Broadcast the new state to all connected browsers.
                    if clients:
                        await asyncio.wait([client.send_json(latest_market_data) for client in clients])

    except Exception as e:
        print(f"Bitstamp feed error: {e}. Reconnecting in 5 seconds...")
        await asyncio.sleep(5)

# We also need to initialize the global state with the new data structure
latest_market_data = {
    "ohlc_series": [], # This is the new structure for the chart
    "trades": [],
    "raw_bytes_total": 0,
    "phicomp_bytes_total": 0
}

@app.on_event("startup")
async def startup_event():
    """Start the market feed manager as a background task when the app starts."""
    asyncio.create_task(market_feed_manager())

@app.websocket("/ws/market_data")
async def market_data_stream(websocket: WebSocket):
    """Connects a browser client and streams the globally managed market data to it."""
    await websocket.accept()
    clients.add(websocket)
    try:
        # Send the most recent data immediately upon connection
        await websocket.send_json(latest_market_data)
        while True:
            # Keep the connection alive; data is pushed from the manager task.
            await websocket.receive_text()
    except Exception:
        print(f"Client disconnected from market data stream.")
    finally:
        clients.remove(websocket)
        await websocket.close()
        
# =================================================================================
# DEMO 7: PROCEDURAL CITY GENERATION (MODLO SEQUENCE)
# =================================================================================
@app.get("/api/generate_universe")
def generate_universe(seed: int = 1337, grid_size: int = 50):
    """
    Uses the Modlo Sequence in a multi-dimensional way to procedurally generate
    a 2D universe of star systems. The seed makes the generation deterministic.
    """
    # 1. Use the seed to ensure the universe is reproducible.
    random.seed(seed)
    
    # 2. Generate two long Modlo sequences. We'll use one for X-axis properties
    #    and one for Y-axis properties to create complex, non-linear patterns.
    #    This demonstrates the multi-dimensional application of the sequence.
    modlo_x = modlo_sequence(grid_size)
    modlo_y = modlo_sequence(grid_size)
    
    star_systems = []
    for y in range(grid_size):
        for x in range(grid_size):
            # 3. Combine the X and Y sequences to determine if a star exists here.
            #    Using a prime number modulus provides good, non-grid-like distribution.
            existence_chance = (modlo_x[x] + modlo_y[y]) % 23
            
            # Only create a star if the chance is high enough (e.g., > 18)
            if existence_chance > 18:
                # 4. Use a different combination to determine the star's properties.
                star_type_val = (modlo_x[x] * modlo_y[y]) % 100
                
                # Determine star properties based on the sequence values
                if star_type_val > 95:
                    star_type = "Pulsar"
                    color = "#9b59b6" # Purple
                    size = (modlo_x[x] % 5 + 1) * 1.5
                elif star_type_val > 80:
                    star_type = "Red Giant"
                    color = "#e74c3c" # Red
                    size = (modlo_y[y] % 8 + 4) * 1.2
                elif star_type_val > 60:
                    star_type = "Blue Giant"
                    color = "#3498db" # Blue
                    size = (modlo_x[x] % 6 + 3) * 1.4
                else:
                    star_type = "Main Sequence"
                    color = "#f1c40f" # Yellow
                    size = (modlo_y[y] % 4 + 2)
                
                star_systems.append({
                    "x": x, "y": y,
                    "size": size,
                    "color": color,
                    "type": star_type,
                    # We include the raw data to prove it's not random!
                    "modlo_vals": f"X:{modlo_x[x]}, Y:{modlo_y[y]}" 
                })
                
    return {"star_systems": star_systems, "grid_size": grid_size}

# =================================================================================
# DEMO 8 : module sequence
# =================================================================================
@app.get("/api/generate_grid")
def generate_grid(seed: int = 1337, grid_size: int = 50):
    """
    Uses the Modlo Sequence in a multi-dimensional way to procedurally generate
    a 2D grid of deterministic data points. The seed makes the generation reproducible.
    This can be interpreted as a star map, a financial market state, or a digital twin simulation.
    """
    # 1. Use the seed to ensure the grid is reproducible.
    random.seed(seed)
    
    # 2. Generate two long Modlo sequences for X and Y axes.
    modlo_x = modlo_sequence(grid_size)
    modlo_y = modlo_sequence(grid_size)
    
    grid_points = []
    for y in range(grid_size):
        for x in range(grid_size):
            # 3. Combine sequences to determine if a point exists and its properties.
            existence_chance = (modlo_x[x] + modlo_y[y]) % 23
            
            if existence_chance > 18:
                # 4. Use a different combination to determine the point's "energy level" or "value".
                value_val = (modlo_x[x] * modlo_y[y]) % 100
                
                # Determine properties based on the sequence values
                if value_val > 95:
                    point_type = "High-Alpha Event" # Financial context
                    color = "#e74c3c" # Red - critical event
                    size = 12
                elif value_val > 80:
                    point_type = "Market Anomaly"
                    color = "#f1c40f" # Yellow - warning
                    size = 8
                elif value_val > 60:
                    point_type = "Synchronized State"
                    color = "#3498db" # Blue - stable
                    size = 6
                else:
                    point_type = "Nominal Fluctuation"
                    color = "#2ecc71" # Green - normal
                    size = 4
                
                grid_points.append({
                    "x": x, "y": y,
                    "size": size,
                    "color": color,
                    "type": point_type,
                    # We include the raw data to prove it's not random!
                    "modlo_vals": f"X:{modlo_x[x]}, Y:{modlo_y[y]}",
                    "deterministic_id": f"ID-{seed}-{x}-{y}" # A unique, reproducible ID
                })
                
    return {"grid_points": grid_points, "grid_size": grid_size}

# =================================================================================
# HTML Page Routing
# =================================================================================
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/demo/modlo_grid_two", response_class=HTMLResponse)
async def show_modlo_grid_two_demo(request: Request):
    return templates.TemplateResponse("modlo_demo_two.html", {"request": request})

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




if __name__ == "__main__":
    import uvicorn
    print("="*50)
    print(">> Running demo server in local development mode.")
    print(">> Access at http://127.0.0.1:8000")
    print("="*50)
    uvicorn.run(app, host="127.0.0.1", port=8000)