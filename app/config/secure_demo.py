from kombu import Queue

# 定义数据库信息
SQLALCHEMY_DATABASE_URI = ""
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 定义flask信息
SECRET_KEY = '123'

# 定义celery信息
BROKER_URL = ''
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_QUEUES = (
    Queue("task", routing_key="task"),
    Queue("task_single", routing_key="task_single")
)
CELERY_ROUTES = {
    'tasks.task_f': {
        'queue': 'task',
        'routing_key': 'task',
    },
    'tasks.task_single_f': {
        'queue': 'task_single',
        'routing_key': 'task_single',
    },
}

# 定义账号
ZUCC_ID = ''
ZUCC_PASSWORD = ''
LUOGU_ID = ''
LUOGU_PASSWORD = ''
