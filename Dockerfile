# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Clone the GitHub repository
RUN apt-get update && apt-get install -y git \
    && git clone https://github.com/ColorfulCookie/coffee-counter /app

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-cors

# Expose the port the Flask app runs on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "coffe_server.py"]