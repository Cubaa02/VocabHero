#!/usr/bin/env bash
set -e

# čeká na DB (pomocí jednoduchého Python skriptu)
python /app/wait_for_db.py

echo "Spouštím migrace..."
python manage.py migrate --noinput

# pokud chceš collectstatic v dev, můžeš ho zapnout, zatím ho nenechávám automaticky
# python manage.py collectstatic --noinput

# start dev server nebo gunicorn podle env
if [ "$DJANGO_DEBUG" = "True" ] || [ "$DJANGO_DEBUG" = "true" ]; then
  echo "Spouštím Django dev server..."
  python manage.py runserver 0.0.0.0:8000
else
  echo "Spouštím gunicorn..."
  exec gunicorn vocabhero.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi
