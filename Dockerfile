# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Set default environment variables for credentials
ENV COFFEE_USERNAME=admin
ENV COFFEE_PASSWORD=password

# Clone the GitHub repository
RUN apt-get update && apt-get install -y git \
    && git clone https://github.com/ColorfulCookie/coffee-counter /app

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-cors flask-login gunicorn

# Expose the port the Flask app runs on
EXPOSE 5000

# Command to run the Flask application with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "coffe_server:app"]