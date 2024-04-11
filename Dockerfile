# Use an official Python runtime as a parent image # 3.10 is the python version I am using
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install Poetry, Poetry is a Python dependency management tool
RUN pip install --no-cache-dir poetry

# Use Poetry to install dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Make port 5000 available to the world outside this container
EXPOSE 5001

# Run start.sh when the container launches
CMD ["./start.sh"]