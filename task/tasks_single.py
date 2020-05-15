from celery import Celery, platforms

from app.config.secure import BROKER_URL

platforms.C_FORCE_ROOT = True
celery = Celery('task-single')
celery.config_from_object('app.config.secure')
celery.conf['BROKER_URL'] = BROKER_URL


@celery.task
def task_single_f(func, **kwargs):
    from app import create_app
    with create_app().app_context():
        print(func, kwargs)
        func(**kwargs)
