## Download files queue

### Installation
 - Install Redis in system
```bash 
sudo apt install redis
```
 - Install requirements in virtualenv
```bash
pip install celery redis
```

### Setup project path
 - Export:
```bash
export PYTHONPATH=/home/debashis/works/dissertation:$PYTHONPATH
```
### Run celery worker from project directory
 - Celery worker:
```bash
celery -A celery_app.task worker --concurrency=1 -l INFO
```