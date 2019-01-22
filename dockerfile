# Use an official Python runtime as a parent image
FROM python:3.7.2-slim

# install necessary packages/libraries
RUN apt-get update && apt-get install -y \
curl \
jq

# Set the working directory to /app & copy contents to /app
WORKDIR /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# make bash script executable
RUN chmod 777 arrests.sh

# make some variables for github
# dockerfile requires defaults, so include dummy data here
ENV GITHUB_KEY 1234
ENV GITHUB_USER abcd
ENV CI_TYPE null
 
# Run script when the container launches
CMD /app/arrests.sh $GITHUB_USER $GITHUB_KEY
