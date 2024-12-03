# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install Flask

# Expose the default port for Cloud Run
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]