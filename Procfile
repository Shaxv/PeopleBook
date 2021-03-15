web: daphne django_blog.asgi:application --port $PORT --bind 0.0.0.0 -v2
chatworker: python manage.py runworker --settings=django_blog.settings -v2