# 定义数据库信息
SQLALCHEMY_DATABASE_URI = r"sqlite:///../view-oj.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 定义flask信息
SECRET_KEY = 'view-oj'

# 定义celery信息
BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Asia/Shanghai'

# 定义redis信息
REDIS_URL = 'redis://127.0.0.1:6379/0'
