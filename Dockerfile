# Set arguments
ARG BASE_PATH
ARG BASE_CONTAINER=python:3.8

# Set the base image. 
FROM --platform=linux/amd64 $BASE_CONTAINER

# Sets the user name to use when running the image.
RUN apt-get update && apt-get install -y && apt-get clean

# Make a directory for our app
RUN mkdir /app
WORKDIR /app

# Install dependencies
COPY $BASE_PATH/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy our source code
COPY $BASE_PATH/*.py .

# Run the application
ENTRYPOINT ["python", "app.py"]
