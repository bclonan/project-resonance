
#!/usr/bin/env python3
import sys
import os

# Add the resonance_demos directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resonance_demos'))

# Import and run the app
from app import app
import uvicorn

if __name__ == "__main__":
    print("Starting Project Resonance Demos...")
    uvicorn.run(app, host="0.0.0.0", port=5000)
