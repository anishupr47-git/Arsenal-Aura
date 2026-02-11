python manage.py migrate
python manage.py seed
gunicorn arsenal_aura.wsgi:application --bind 0.0.0.0:$PORT
