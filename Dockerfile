# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code



# Copy requirements.txt and install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port on which the Flask app runs
EXPOSE 5000

# Set environment variables (optional but recommended)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
