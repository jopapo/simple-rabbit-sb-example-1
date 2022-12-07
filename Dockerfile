# Set arguments
ARG base_container=python:3.8

# Set the base image. 
FROM --platform=linux/amd64 $base_container

# Sets the user name to use when running the image.
RUN apt-get update && apt-get install -y && apt-get clean

# Make a directory for our app
RUN mkdir /app
WORKDIR /app

# Install dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# Copy our source code
COPY app/ ./

# Run the application
ENTRYPOINT ["python"]