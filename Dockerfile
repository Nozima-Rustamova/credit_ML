# Dockerfile
FROM python:3.11-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set workdir
WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files (if needed)
RUN python manage.py collectstatic --noinput

# expose port
EXPOSE 8000

# default command
CMD ["gunicorn", "credit_risk.wsgi:application", "--bind", "0.0.0.0:8000"]
