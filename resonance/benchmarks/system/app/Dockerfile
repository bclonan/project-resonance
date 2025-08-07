# Use an official, slim Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir makes the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY main.py .

# Define the command to run the application
# uvicorn is a high-performance ASGI server
# --host 0.0.0.0 makes the server accessible from outside the container
# --workers 4 will run 4 worker processes to handle more concurrent requests
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]