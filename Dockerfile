# Dockerfile
FROM ubuntu:24.04

# Install Python + venv tooling and system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-venv \
    python3-pip \
    build-essential \
    libssl-dev \
    libffi-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create & activate venv
RUN python3 -m venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first to leverage caching
COPY requirements.txt /app/

# Install Python packages into the venv
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Set the entry point for the application
CMD ["python", "src/main.py"]
