import time
from datetime import datetime
from flask import Flask
from tasks import async_task

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello Celery'


@app.route('/celery')
def celery():
    async_task.delay()
    return "celery is done"