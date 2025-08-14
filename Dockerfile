# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and browsers
RUN playwright install --with-deps

# Copy project files
COPY . .

# Create reports directory
RUN mkdir -p reports

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash testuser && \
    chown -R testuser:testuser /app
USER testuser

# Expose port for Locust web UI
EXPOSE 8089

# Default command
CMD ["pytest", "tests/", "-v"]