# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy requirements.txt and install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the Flask app port
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
