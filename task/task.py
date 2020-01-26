from app import create_app
from task.base import make_celery

app = create_app()
celery = make_celery(app)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3600, name='1111',
                             sig=task_f,
                             args=[])


@celery.task
def task_f(func, **kwargs):
    return func(kwargs)
