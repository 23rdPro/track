web: bin/start-nginx bin/start-pgbouncer gunicorn -c gunicorn.conf track.wsgi:application --log-file -

worker: celery -A track worker -l info
