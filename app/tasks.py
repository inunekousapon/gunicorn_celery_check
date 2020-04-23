from celery import Celery
import time
from celery_redis_sentinel.task import EnsuredRedisTask
from celery_redis_sentinel import register


register()
celery = Celery('tasks')

BROKER_TRANSPORT_OPTIONS = {
    'sentinels': [('redis-sentinel', 26379)],
    'service_name': 'mymaster',
    'socket_timeout': 0.1,
}
celery.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    BROKER_URL='redis-sentinel://redis-sentinel:26379/0',
    BROKER_TRANSPORT_OPTIONS = BROKER_TRANSPORT_OPTIONS,
    CELERY_RESULT_BACKEND = 'redis-sentinel://redis-sentinel-cluster:26379/1',
    CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = BROKER_TRANSPORT_OPTIONS,
    CELERY_RESULT_SERIALIZER='json',
)

@celery.task(name="setTask", base=EnsuredRedisTask)
def async_task():
    print("60 seconds sleep!!")
    time.sleep(10)
    print("10 seconds...")
    time.sleep(10)
    print("20 seconds...")
    time.sleep(10)
    print("30 seconds...")
    time.sleep(10)
    print("40 seconds...")
    time.sleep(10)
    print("50 seconds...")
    time.sleep(10)
    print("I'm wake up!")
    return