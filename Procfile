web: python manage.py collectstatic --noinput; newrelic-admin run-program gunicorn -w 4 -b 0.0.0.0:$PORT -k gevent gamelog.wsgi
