from flask_cors import CORS
from flask_login import LoginManager
from flask_redis import FlaskRedis

from app.models.base import db

from .app import Flask

cors = CORS(supports_credentials=True)
login_manager = LoginManager()
redis1 = FlaskRedis(config_prefix="REDIS_1")
redis2 = FlaskRedis(config_prefix="REDIS_2")


def register_blueprints(flask_app):
    from app.api.v2 import create_blueprint_v2
    flask_app.register_blueprint(create_blueprint_v2(), url_prefix='/v2')


def register_plugin(flask_app):
    # 注册sqlalchemy

    db.init_app(flask_app)

    # 初始化数据库
    with flask_app.app_context():
        db.create_all()

    # 注册cors
    cors.init_app(flask_app)

    # 注册用户管理器
    login_manager.init_app(flask_app)

    # 注册redis
    redis1.init_app(flask_app)
    redis2.init_app(flask_app)


def create_app():
    flask_app = Flask(__name__)

    # 导入配置
    flask_app.config.from_object('app.config.setting')
    flask_app.config.from_object('app.config.secure')

    register_blueprints(flask_app)
    register_plugin(flask_app)

    return flask_app
