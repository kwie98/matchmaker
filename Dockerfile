FROM python:3.12.1-alpine3.19
WORKDIR /app

# Python deps:
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Node deps:
RUN apk add --no-cache npm=10.2.5-r0 &&\
    rm -rf /var/apk/cache/*

# Source:
COPY ./asgi.py ./manage.py ./settings.py ./urls.py ./wsgi.py ./
COPY ./matchmaker ./matchmaker
COPY ./theme ./theme

# Build tailwind styles:
RUN ./manage.py tailwind install &&\
    ./manage.py tailwind build &&\
    ./manage.py collectstatic

CMD ["daphne", "asgi:application", "-b", "0.0.0.0", "-p", "8000"]
