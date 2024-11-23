# Use the official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Flask application
COPY . .

# Expose port for Flask app
EXPOSE 5000

# Command to run Flask application
CMD ["python", "app.py"]
