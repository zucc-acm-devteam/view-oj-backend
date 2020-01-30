from celery import Celery, platforms

from app.libs.service import task_calculate_user_rating
from app.libs.spider_service import task_crawl_accept_problem

platforms.C_FORCE_ROOT = True
celery = Celery('tasks')
celery.config_from_object('app.config.setting')
celery.config_from_object('app.config.secure')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3600, name='task_crawl_accept_problem',
                             sig=task_f,
                             args=[task_crawl_accept_problem])
    sender.add_periodic_task(3600 * 4, name='task_calculate_user_rating',
                             sig=task_f,
                             args=[task_calculate_user_rating])


@celery.task
def task_f(func, **kwargs):
    from app import create_app
    with create_app().app_context():
        func(**kwargs)
