FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY . /code/

WORKDIR /code/jbl_chat

RUN ./manage.py collectstatic --noinput
RUN ./manage.py migrate
RUN ./manage.py loaddata fixtures/local_development_users.json
RUN ./manage.py set_default_passwords
RUN ./manage.py make_messages_fixture
RUN ./manage.py loaddata messages_fixture.json

## Use Gunicorn to run the application.
CMD gunicorn jbl_chat.wsgi:application --bind 0.0.0.0:${PORT:-8000}