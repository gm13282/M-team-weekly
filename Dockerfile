# Use an official Python runtime as a parent image
FROM python:3.12.4-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY /app/ /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create logs directory
RUN mkdir -p /app/logs

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD ["python", "main.py"]