# Use a stable, slim Python 3.12 image
FROM python:3.12-slim

# Install system dependencies needed for pymssql and psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Keep the container alive or run the script
CMD ["python", "-m", "scripts.load_test"]