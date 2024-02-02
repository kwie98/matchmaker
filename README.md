# Matchmaker

Create random round robin tournaments with randomized teams and track scores on a scoreboard.

## Develop

**Important**: In _dev_ and _prod_, certain env variables need to be set (see [docker-compose.yaml](docker-compose.yaml)). In _prod_, `docker compose` reads these from a `.env` file in the project root. For _dev_, you can set the environment variables manually or also use an `.env` file with [direnv](https://github.com/direnv/direnv).

```bash
# Initial setup:
python -m venv venv             # minimum python version: 3.12 (older versions could work as well)
pip install -r requirements.txt # python dependencies
./manage.py tailwind install    # tailwind (node) dependencies (requires a npm installation)
./manage.py migrate             # init db

# Start dev server:
./manage.py runserver
./manage.py tailwind start
```

## Deploy

- init db
- generate a secret key and adjust `.env` accordingly
- allow through firewall: `sudo ufw allow 80,443/tcp`
- port forward

### HTTPS

- <https://mpolinowski.github.io/docs/DevOps/NGINX/2020-08-28--nginx-docker-certbot/2020-08-27/>
- `certbot certonly --standalone` while server is not running

## Stack

- Django backend
- HTML/TailwindCSS/HTMX frontend
- Nginx server
- Docker

### Tasks

- Clear expired sessions from the db regularly (`./manage.py clearsessions`) <https://docs.djangoproject.com/en/5.0/topics/http/sessions/>
- renew cert: `certbot renew`
- renew domain
