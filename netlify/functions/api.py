# This file is the serverless entry point for Netlify.
# It imports your existing FastAPI app and wraps it with Mangum.

import sys
from os import path
import mangum

# Add the demo app's directory to the Python path
# This allows us to import the 'app' object from resonance_demos/app.py
sys.path.append(path.abspath(path.join(path.dirname(__file__), '../../resonance_demos')))

# Import your existing FastAPI application
from app import app

# Create the Mangum handler. This is the adapter that allows FastAPI
# to run in a serverless environment (like AWS Lambda, which Netlify uses).
handler = mangum.Mangum(app, lifespan="off")