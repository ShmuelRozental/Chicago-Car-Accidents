# Use a lightweight Python base image
FROM python:3-slim

# Expose the application port
EXPOSE 5002

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off output buffering for logs
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements first to leverage Docker's caching mechanism
COPY requirements.txt /app/

# Install dependencies
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code into /app
COPY . .

# Create a non-root user with access to /app
RUN adduser --uid 5678 --disabled-password --gecos "" appuser && \
    chown -R appuser /app

# Switch to the non-root user
USER appuser

# Set the default command to run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "app:app"]
