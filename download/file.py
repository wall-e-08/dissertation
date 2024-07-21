import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from .task import download_queue


def from_url(url, save_directory, base_path,
             bs4kwargs, ignore_anchor_value_list=[],
             file_filter_function=lambda x: True):
  os.makedirs(save_directory, exist_ok=True)
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  # Find the specific section with css id
  try:
    target_section = soup.find(bs4kwargs)
  except:
    print(f"Error: wrong input '{bs4kwargs}'")
    return
  if not target_section:
    print(f"Error: No section with '{bs4kwargs}' found in {url}")
    return
  for link in target_section.find_all('a'):
    href = link.get('href')
    if not href:
      continue

    full_url = urljoin(url, href)
    path = urlparse(full_url).path

    if not link.string or link.string.lower() in ignore_anchor_value_list or not path or path == '/':
      continue

    if path.endswith('/'):
      # It's a directory, recurse into it
      from_url(full_url, os.path.join(save_directory, href), base_path,
                bs4kwargs, ignore_anchor_value_list, file_filter_function)
    else:
      # It's a file link, check extension and download if valid
      file_url = urljoin(url, href)
      if file_filter_function(file_url):
        print(f"sending queue: {file_url}")
        download_queue.delay(file_url, save_directory)
      else:
        print(f"Skipping by filter: {file_url}")

