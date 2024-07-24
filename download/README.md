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
 - Start celery task queue:
```bash
celery -A celery_app worker --concurrency=1 -l INFO
 
```
 - Purge all task:
```bash
celery -A celery_app purge -f
```
 - Check pending task:
```bash
celery -A celery_app inspect active
```
