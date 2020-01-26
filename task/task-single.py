from app import create_app
from task.base import make_celery

app = create_app()
celery = make_celery(app)


@celery.task
def task_f(func, **kwargs):
    return func(kwargs)
