from celery import Celery, Task

app = Celery('task', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

app.conf.update(
  task_serializer='json',
  accept_content=['json'],
  result_serializer='json',
  timezone='UTC',
  enable_utc=True,
)

class CallbackTask(Task):
  def on_success(self, retval, task_id, args, kwargs):
    '''
    retval – The return value of the task.
    task_id – Unique id of the executed task.
    args – Original arguments for the executed task.
    kwargs – Original keyword arguments for the executed task.
    '''
    print(f"Finished task: {task_id}")

  def on_failure(self, exc, task_id, args, kwargs, einfo):
    '''
    exc – The exception raised by the task.
    task_id – Unique id of the failed task.
    args – Original arguments for the task that failed.
    kwargs – Original keyword arguments for the task that failed.
    '''
    print(f"Failed task {task_id}", exc)


import download.task