import os
import requests
from urllib.parse import urlparse
from celery_app.task import app


@app.task(name='download.task.download_queue', default_retry_delay=1 * 60) # retry after 1min
def download_queue(_url, _dir):
  print(f"Added download queue: {_url}")
  # Extract filename from URL
  parsed_url = urlparse(_url)
  filename = os.path.basename(parsed_url.path)

  # Ensure the save path is not a directory or if the file already exists
  _file_path = os.path.join(_dir, filename)
  if os.path.isdir(_file_path) or os.path.exists(_file_path):
    print(f"Skipping (file exists): {_file_path}")
    return

  response = requests.get(_url)

  if response.headers.get('Content-Type'):
    content_type = response.headers.get('Content-Type')
    if not content_type or 'text/html' in content_type:
      print(f"Skipping(not file): {_url}")
      return True
  else:
    print(f"Skipping(not file): {_url}")
    return True

  with open(_file_path, 'wb') as f:
    f.write(response.content)
    print(f"Downloaded {filename}...")
  return True
