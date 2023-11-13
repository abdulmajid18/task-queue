# Use the official Python image as the base image
FROM python:3.11.1-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create a directory for your application and set it as the working directory
WORKDIR /app

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy the requirements file to the container
COPY requirements-task.txt .

# Install the Python dependencies
RUN pip install -r requirements-task.txt

# Copy the Python script and entrypoint script to the container
COPY task.py .
COPY entrypoint.sh .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose any necessary ports (if applicable)
 EXPOSE 1800


# Define the entrypoint script to start your RPC server
CMD ["python", "task.py"]

