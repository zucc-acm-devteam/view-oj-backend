# 定义数据库信息
SQLALCHEMY_DATABASE_URI = r"sqlite:///../view-oj.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 定义flask信息
SECRET_KEY = 'view-oj'

# 定义celery信息
BROKER_1_URL = 'sqla+sqlite:///view-oj-celery1.db'
BROKER_2_URL = 'sqla+sqlite:///view-oj-celery2.db'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Asia/Shanghai'

# 定义redis信息
REDIS_1_URL = 'redis://127.0.0.1:6379/1'
REDIS_2_URL = 'redis://127.0.0.1:6379/2'

# 定义账号
VJUDGE_ID = '2013300116'
VJUDGE_PASSWORD = '8520967123'
LUOGU_ID = '18768153531'
LUOGU_PASSWORD = '990718'
