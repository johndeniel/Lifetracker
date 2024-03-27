# Use the official Python 3.12 image with Alpine Linux 3.18 as the base image
FROM python:3.12.0rc1-alpine3.18 as base

# Set the working directory inside the container to /code
WORKDIR /code

# Install build dependencies and Python dependencies specified in requirements.txt
COPY ./requirements.txt /code/requirements.txt
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    libressl-dev \
    libressl3.4-libcrypto \
 && pip install --no-cache-dir --upgrade -r /code/requirements.txt \
 && apk del .build-deps

# Copy all files from your host to the /code directory inside the container
COPY . .

# Expose port 7860 to allow external connections to your FastAPI application
EXPOSE 7860

# Define the command to run when the container starts
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
