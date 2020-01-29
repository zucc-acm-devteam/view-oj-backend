from celery import Celery

from app import create_app

celery = Celery('tasks-single')
celery.config_from_object('app.config.setting')
celery.config_from_object('app.config.secure')


@celery.task
def task_single_f(func, **kwargs):
    with create_app().app_context():
        func(kwargs)
