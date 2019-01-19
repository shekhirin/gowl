#!/bin/sh
#!/bin/bash

NAME="goalboard_app"
DJANGODIR=/root/goalboard
NUM_WORKERS=3
DJANGO_WSGI_MODULE=goalboard.wsgi

echo "Starting $NAME"

cd $DJANGODIR
source venv/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=goalboard.settings
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export DEBUG=False


$DJANGODIR/venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --log-level=debug \
  --log-file=-
