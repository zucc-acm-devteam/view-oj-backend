from kombu import Queue

# 定义数据库信息
SQLALCHEMY_DATABASE_URI = ""
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 定义flask信息
SECRET_KEY = '123'

# 以下两行如果需要允许跨域则添加，防止chrome禁止
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_SAMESITE = 'None'

# 定义celery信息
BROKER_URL = ''
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_QUEUES = (
    Queue("task", routing_key="task"),
    Queue("task_single", routing_key="task_single")
)
CELERY_ROUTES = {
    'tasks.crawl_accept_problem_schedule_task': {
        'queue': 'task',
        'routing_key': 'task',
    },
    'tasks.calculate_user_rating_schedule_task': {
        'queue': 'task',
        'routing_key': 'task',
    },
    'tasks.crawl_course_info_schedule_task': {
        'queue': 'task',
        'routing_key': 'task',
    },
    'tasks.crawl_accept_problem_task': {
        'queue': 'task',
        'routing_key': 'task',
    },
    'tasks.calculate_user_rating_task': {
        'queue': 'task',
        'routing_key': 'task',
    },
    'tasks.crawl_problem_rating_task': {
        'queue': 'task',
        'routing_key': 'task',
    },
    'tasks.crawl_course_info_task': {
        'queue': 'task',
        'routing_key': 'task',
    },
    'tasks.crawl_accept_problem_task_single': {
        'queue': 'task_single',
        'routing_key': 'task_single',
    },
}

# 定义账号
ZUCC_ID = ''
ZUCC_PASSWORD = ''
LUOGU_ID = ''
LUOGU_PASSWORD = ''
