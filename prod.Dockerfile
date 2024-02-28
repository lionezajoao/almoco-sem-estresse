# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install pipenv
RUN pip install pipenv

# Copy the Pipfile and Pipfile.lock into the container at /usr/src/app
COPY Pipfile Pipfile.lock ./

# Install dependencies from the Pipfile
RUN pipenv install

# Copy the rest of your application's code
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the FastAPI app
CMD ["pipenv", "run", "prod"]
