# Use the official Python slim image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install system dependencies and Python dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

# Copy the wait-for-it.sh script and the Python script into the container
COPY wait-for-it.sh /app/wait-for-it.sh
COPY producer.py /app/producer.py

# Make the wait-for-it.sh script executable
RUN chmod +x /app/wait-for-it.sh

# Define the command to run the application
CMD ./wait-for-it.sh -s -t 30 "$ZOOKEEPER_SERVER" -- ./wait-for-it.sh -s -t 30 "$KAFKA_SERVER" -- python -u producer.py
