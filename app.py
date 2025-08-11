from resonance_demos.app import app

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI application exposed as `app`
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
