#!/bin/sh


set -o errexit
set -o nounset

 jupyter notebook --port=8000 --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='123456'

#rm -f './celerybeat.pid'
#celery worker --app=celery_app.app:app --loglevel=debug --concurrency=1 \
#-Ofair --pool=eventlet --hostname=worker@%h & \
#celery --app=celery_app.app:app beat -l info

exec "$@"
