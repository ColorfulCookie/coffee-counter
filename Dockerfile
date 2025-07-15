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

# Clone the GitHub repository
RUN apt-get update && apt-get install -y git \
    && git clone https://github.com/ColorfulCookie/coffee-counter /app

# Checkout to lastest commit
RUN cd /app && git checkout

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-cors flask-login flask-limiter flask-wtf gunicorn

# Expose the port the Flask app runs on
EXPOSE 5000

# Volume for the database
VOLUME ["/data"]

# Command to run the Flask application with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "coffee_server:app"]