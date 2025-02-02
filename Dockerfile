FROM python:3.12.8-slim

# Exposing port
EXPOSE 8545

# Setting working directory
WORKDIR /app

# Install psycopg2 dependencies
RUN apt update \
    && apt -y install libpq-dev gcc

# Copying source code
COPY requirements.txt .

# Installing dependencies
RUN pip install -r /app/requirements.txt

# Copy the FastAPI application
COPY . .

WORKDIR /app/src

# Running application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8545"]
