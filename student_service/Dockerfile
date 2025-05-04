# Use the official Python image as the base image
FROM python:3.9-slim

RUN apt-get update
RUN apt-get install curl telnet dnsutils -y
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["python3", "app.py"]