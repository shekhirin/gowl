#!/bin/sh
#!/bin/bash

NAME="gowl_app"
DJANGODIR=/root/gowl
NUM_WORKERS=3
DJANGO_WSGI_MODULE=gowl.wsgi

echo "Starting $NAME"

cd $DJANGODIR
source venv/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=gowl.settings
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

set -a
. ./.env
set +a

python manage.py migrate
python manage.py collectstatic --noinput --exclude-dirs admin

$DJANGODIR/venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --log-level=debug \
  --log-file=- \
  --bind=127.0.0.1:$1
