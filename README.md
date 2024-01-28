# Matchmaker

Create a tournament with randomized teams and track its progress.

## Stack

- Django backend
- Pure HTML/TailwindCSS frontend

## Install

```bash
python -m venv venv
pip install -r requirements.txt # python dependencies
./manage.py tailwind install    # tailwind (node) dependencies
```

## Develop

```bash
./manage.py runserver
./manage.py tailwind start
```

## Deploy

- init db
- generate `SECRET_KEY` (.env)
- allow through firewall: `sudo ufw allow 80,443/tcp`
- port forward

### HTTPS

- <https://mindsers.blog/en/post/https-using-nginx-certbot-docker/>
- For first time, nginx container will probably crash because the certificates are not there for the second (443) server. Comment out its block and generate the certs, then uncomment it

## Todo

- pause = keine radios
- fix static volume bug
- make data structures nicer
- future rounds not changeable
- spinners for radio buttons
- sanitize user input (names)
- block overwriting ongoing tournament?
- trim requirements
- pre-commit formatting, linting
- assert `./manage.py check --deploy` clean on deploy!

### Tasks

- Clear expired sessions from the db regularly (`./manage.py clearsessions`) <https://docs.djangoproject.com/en/5.0/topics/http/sessions/>
- renew cert: `docker compose run --rm certbot renew`
- renew domain
