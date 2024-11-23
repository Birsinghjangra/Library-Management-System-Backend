# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y unixodbc-dev
RUN apt-get install -y ca-certificates
RUN apt-get install -y telnet
RUN apt-get install -y vim
RUN apt-get clean

# Set the working directory within the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "app.py"]