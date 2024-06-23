# Use the official Python image from the Docker Hub
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the .env file
COPY .env .env

# Install python-dotenv
RUN pip install python-dotenv

# Command to run the application
CMD ["python", "main.py"]
