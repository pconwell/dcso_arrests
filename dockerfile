# Use an official Python runtime as a parent image
FROM python:3.7.2-slim

RUN apt-get update && apt-get install -y \
curl \
jq

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN chmod 777 arrests.sh

# make data persistant
VOLUME ["/data"]

# Run app.py when the container launches
CMD /app/arrests.sh
