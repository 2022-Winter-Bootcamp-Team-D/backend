# backend/Dockerfile
# set base image
FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /backend
WORKDIR /backend

COPY ./backend/ /backend/
COPY . /backend/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# EXPOSE 8000

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 