FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies for mysqlclient and netcat
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . ./

# Run migrations before starting Django server
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000