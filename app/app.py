import time
from datetime import datetime
from flask import Flask

app = Flask(__name__)

from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# update flask config to use celery
app.config.update(
    CELERY_BROKER_URL='redis://redis:6379',
    CELERY_RESULT_BACKEND='redis://redis:6379',
    CELERYD_HIJACK_ROOT_LOGGER=False
)
celery = make_celery(app)


@celery.task()
def async_task():
    #time.sleep(10)
    dt = datetime.now().isoformat()
    with open('/tmp/' + dt, 'w') as w:
        w.write("async")
    return dt

@app.route('/')
def index():
    return 'Hello Celery'


@app.route('/celery')
def celery():
    async_result = async_task.delay()
    app.logger.error("celery!!!")
    return async_result.get()