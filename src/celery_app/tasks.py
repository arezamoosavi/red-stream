import logging

from celery import current_task
from celery.schedules import crontab

from .app import app as celery_app


# logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | {%(pathname)s:%(lineno)d} | %(module)s | %(levelname)s | %(funcName)s | %(message)s",
)


@celery_app.task
def testsss(arg):
    print(arg)


celery_app.conf.beat_schedule = {
    "add-every-5-seconds": {
        "task": "celery_app.tasks.testsss",
        "schedule": 5.0,
        "args": ("hi",),
    },
}
