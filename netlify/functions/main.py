import sys
from pathlib import Path

# Add the project root to the Python path to allow imports from other directories
# This is necessary so that 'from resonance_demos.app import app' works correctly.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from mangum import Mangum
from resonance_demos.app import app

# Mangum is an adapter that allows your FastAPI (ASGI) application
# to run in a serverless environment like AWS Lambda, which Netlify uses.
handler = Mangum(app, lifespan="off")