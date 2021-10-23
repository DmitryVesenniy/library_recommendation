from celery import Celery
from celery.schedules import crontab

from start_train import main

celery_app = Celery(__name__, broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")
celery_app.conf.task_routes = {"train_task": "main-queue"}

celery_app.conf.beat_schedule = {
    "train_worker": {
        "task": "create_task",
        "schedule": crontab(hour='*/24')
    }
}


@celery_app.task(bind=True)
def create_task(task_type):
    print("*********************************")
    # main()

