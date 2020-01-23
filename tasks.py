from celery import Celery

from app import create_app
from app.libs.service import calculate_user_rating
from app.models.oj import get_oj_list
from app.models.problem import get_problem_by_oj_id
from app.models.user import get_user_list
from app.spiders.oj_spider import crawl_accept_problem, crawl_problem_rating

celery = Celery('tasks')
celery.config_from_object('app.config.setting')
celery.config_from_object('app.config.secure')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3600, task_crawl_all_accept_problem, name='crawl_all_accept_problem')


@celery.task
def task_crawl_all_accept_problem():
    with create_app().app_context():
        user_list = get_user_list()
        for user in user_list:
            for oj in get_oj_list():
                if oj['status'] and user['status']:
                    task_crawl_accept_problem.delay(user['username'], oj['id'])


@celery.task
def task_crawl_accept_problem(username, oj_id):
    with create_app().app_context():
        crawl_accept_problem(username, oj_id)


@celery.task
def task_crawl_problem_rating(problem_id):
    with create_app().app_context():
        crawl_problem_rating(problem_id)


@celery.task
def task_calculate_user_rating(username):
    with create_app().app_context():
        calculate_user_rating(username)


@celery.task
def task_refresh_oj_problem_rating(oj_id):
    with create_app().app_context():
        for i in get_problem_by_oj_id(oj_id):
            task_crawl_problem_rating.delay(i.id)
