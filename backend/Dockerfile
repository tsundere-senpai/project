# # Use an official Python runtime as a parent image
# FROM python:3.8

# # Install required dependencies
# RUN apt-get update && apt-get install -y g++ 

# RUN apt-get install default-jdk

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container
# COPY . /app

# # Install required Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose port 8000 for FastAPI
# EXPOSE 8000

# # Command to run the app
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Use an official Python runtime as a parent image
FROM python:3.8

# Set non-interactive mode for apt-get to prevent prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install required dependencies: g++ for C++, default-jdk for Java
# RUN apt-get update && apt-get install -y \
#     g++ \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
