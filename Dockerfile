# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose the port that the app will run on
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=main.py

# Run the command to start the app
CMD ["flask", "run", "--host=0.0.0.0"]