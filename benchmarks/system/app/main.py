from fastapi import FastAPI, Request
import time
import os

app = FastAPI()

# A simple counter to simulate a unique response for each request
request_counter = 0

@app.get("/")
def read_root(request: Request):
    """
    A simple, fast endpoint that simulates a typical web request.
    It returns a small JSON payload with some identifying information.
    """
    global request_counter
    request_counter += 1
    
    # Simulate a tiny amount of processing work
    time.sleep(0.005) 
    
    return {
        "message": "Service is healthy",
        "hostname": os.getenv("HOSTNAME", "unknown"), # Get the container's hostname
        "request_count": request_counter,
        "client_ip": request.client.host
    }

@app.get("/heavy")
def read_heavy():
    """An endpoint to simulate a more CPU-intensive task."""
    # Simulate a task that takes longer, like a complex database query
    time.sleep(0.05)
    return {"status": "Heavy task complete"}