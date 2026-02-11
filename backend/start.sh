set -e
python manage.py migrate
python manage.py seed
echo "Starting gunicorn on ${PORT:-8000}"
exec python -m gunicorn arsenal_aura.wsgi:application --bind 0.0.0.0:${PORT:-8000}
