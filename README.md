# Matchmaker

Create a tournament with randomized teams and track its progress.

## Stack

- Django backend
- Pure HTML/TailwindCSS frontend

## Install

```bash
python -m venv venv
pip install -r requirements.txt # python dependencies
./manage.py tailwind install # tailwind (node) dependencies
```

## Develop

```bash
./manage.py runserver
./manage.py tailwind start
```

## Todo

- Clear expired sessions from the db regularly (`./manage.py clearsessions`)
  <https://docs.djangoproject.com/en/5.0/topics/http/sessions/>
- sanitize user input (names)
- block overwriting ongoing tournament?
