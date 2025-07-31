# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Set default environment variables for credentials
ENV COFFEE_USERNAME=admin
ENV COFFEE_PASSWORD=password

# Set an environment variable for the database path
ENV COFFEE_DB_NAME=coffee_log.db
ENV DATABASE_PATH=/data/coffee_log.db

# Copy requirements file first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create data directory
RUN mkdir -p /data

# Expose the port the Flask app runs on
EXPOSE 5000

# Volume for the database
VOLUME ["/data"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/login')" || exit 1

# Command to run the Flask application with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "coffee_server:app"]