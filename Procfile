release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn track.wsgi --log-file -
