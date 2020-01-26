from celery import Celery


def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return celery.Task.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
