from celery import Celery, platforms

from app.libs.service import (calculate_user_rating,
                              submit_calculate_user_rating_task)
from app.libs.spider_service import (crawl_accept_problem, crawl_course_info,
                                     crawl_problem_rating,
                                     submit_crawl_accept_problem_task,
                                     submit_crawl_course_info_task)

platforms.C_FORCE_ROOT = True
celery = Celery('tasks')
celery.config_from_object('app.config.secure')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3600, name='crawl_accept_problem_schedule_task',
                             sig=crawl_accept_problem_schedule_task)
    sender.add_periodic_task(3600, name='crawl_course_info_schedule_task',
                             sig=crawl_course_info_schedule_task)
    sender.add_periodic_task(3600 * 4, name='calculate_user_rating_schedule_task',
                             sig=calculate_user_rating_schedule_task)


@celery.task
def crawl_accept_problem_schedule_task():
    from app import create_app
    with create_app().app_context():
        submit_crawl_accept_problem_task()


@celery.task
def calculate_user_rating_schedule_task():
    from app import create_app
    with create_app().app_context():
        submit_calculate_user_rating_task()


@celery.task
def crawl_course_info_schedule_task(course_id):
    from app import create_app
    with create_app().app_context():
        submit_crawl_course_info_task(course_id)


@celery.task
def crawl_accept_problem_task(username, oj_id):
    from app import create_app
    with create_app().app_context():
        crawl_accept_problem(username, oj_id)


@celery.task
def crawl_accept_problem_task_single(username, oj_id):
    crawl_accept_problem_task(username, oj_id)


@celery.task
def calculate_user_rating_task(username):
    from app import create_app
    with create_app().app_context():
        calculate_user_rating(username)


@celery.task
def crawl_problem_rating_task(problem_id):
    from app import create_app
    with create_app().app_context():
        crawl_problem_rating(problem_id)


@celery.task
def crawl_course_info_task(course_id):
    from app import create_app
    with create_app().app_context():
        crawl_course_info(course_id)
