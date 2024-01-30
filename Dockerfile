FROM python:3.12.1-slim-bookworm AS django
WORKDIR /app

ENV VIRTUAL_ENV="/app/venv"
RUN python -m venv "${VIRTUAL_ENV}"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./asgi.py ./manage.py ./settings.py ./urls.py ./wsgi.py ./
COPY ./matchmaker ./matchmaker
COPY ./theme ./theme

CMD ["daphne", "asgi:application", "-b", "0.0.0.0", "-p", "8000"]


FROM python:3.12.1-slim-bookworm AS nodebuilder
WORKDIR /app

COPY --from=django /app ./

ENV VIRTUAL_ENV="/app/venv"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    "npm=9.2.0~ds1-1" \
    && rm -rf /var/lib/apt/lists/*

RUN ./manage.py tailwind install &&\
    ./manage.py tailwind build &&\
    ./manage.py collectstatic


FROM nginx:1.25.3-bookworm AS nginx

COPY --from=nodebuilder /app/static /static
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
