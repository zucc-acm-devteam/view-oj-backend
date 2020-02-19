# 定义数据库信息
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/view-oj"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 定义flask信息
SECRET_KEY = '123456'

# 定义celery信息
BROKER_1_URL = 'redis://127.0.0.1:6379/1'
BROKER_2_URL = 'redis://127.0.0.1:6379/2'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Asia/Shanghai'

# 定义redis信息
REDIS_1_URL = 'redis://127.0.0.1:6379/1'
REDIS_2_URL = 'redis://127.0.0.1:6379/2'

# 定义账号
LUOGU_ID = ''
LUOGU_PASSWORD = ''
