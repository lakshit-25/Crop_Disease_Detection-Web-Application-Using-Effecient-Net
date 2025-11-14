# Use Python base image
FROM python:3.10-slim

# Set working dir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Cloud Run default port
EXPOSE 8080

# Start Flask (ensure app.py contains "app" object)
CMD ["python", "app.py"]
