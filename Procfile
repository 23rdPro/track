web: gunicorn track.wsgi --log-file -
web: bin/start-nginx bundle exec unicorn -c config/unicorn.rb -p $PORT
