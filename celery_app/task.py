from celery import Celery

app = Celery('download_task', broker='redis://localhost:6379')

# class CeleryDownloadTask(celery.Task):
#   pass