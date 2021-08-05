from huey.contrib.djhuey import task
import time

@task()
def add(a, b):
    time.sleep(5)
    return a + b