from celery import Celery, current_task, Task
import time
import os

CELERY_BROKER_URL = os.environ.get(
    'CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL,  # Celery
                backend=CELERY_RESULT_BACKEND)


@celery.task()  # fun_celery註冊
def fun_celery():  # fun_celery
    start = time.perf_counter()
    total = 10
    for current in range(total):
        used = time.perf_counter() - start
        current_task.update_state(state='PROGRESS',
                                  meta={'current': current, 'total': total})
        print(f'\r{current/total:>6.1%}[{"▓"*current}{"-"*(total-current)}]{used:5.2f}s',
              end="", flush=True)
        time.sleep(0.5)
    return "任務完成"


class Test(Task):  # Class_celery
    def run(self):
        start = time.perf_counter()
        total = 10
        for current in range(total):
            used = time.perf_counter() - start
            current_task.update_state(state='PROGRESS',
                                      meta={'current': current, 'total': total})
            print(f'\r{current/total:>6.1%}[{"▓"*current}{"-"*(total-current)}]{used:5.2f}s',
                  end="", flush=True)
            time.sleep(0.5)
        return "任務完成"


cls_celery = celery.register_task(Test())  # Class_celery註冊
