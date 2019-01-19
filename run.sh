#!/bin/sh
#!/bin/bash

NAME="goalboard_app"
DJANGODIR=/root/goalboard
NUM_WORKERS=3
DJANGO_WSGI_MODULE=goalboard.wsgi

echo "Starting $NAME"

cd $DJANGODIR
source ../bin/activate
pip install -r requirementst.xt
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export DEBUG=False


$DJANGODIR/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --log-level=debug \
  --log-file=-
