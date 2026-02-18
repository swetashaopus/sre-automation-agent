FROM python:3.11-slim

# System deps your packages may need (example: build tools, libpq for psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*
  
# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Set the entry point for the application
CMD ["python", "src/main.py"]
