FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY . /code/

WORKDIR /code/jbl_chat

RUN python manage.py collectstatic --noinput

## Use Gunicorn to run the application.
CMD gunicorn jbl_chat.wsgi:application --bind 0.0.0.0:${PORT:-8000}