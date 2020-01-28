from celery import Celery

from app import create_app

celery = Celery('tasks')
celery.config_from_object('app.config.setting')
celery.config_from_object('app.config.secure')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3600, name='1111',
                             sig=task_f,
                             args=[])


@celery.task
def task_f(func, **kwargs):
    with create_app().app_context():
        func(kwargs)
