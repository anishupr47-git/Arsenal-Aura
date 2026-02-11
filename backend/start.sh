python manage.py migrate
python manage.py seed
gunicorn arsenal_aura.wsgi:application
