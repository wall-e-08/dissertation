import mimetypes
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def from_url(url, save_directory, base_path,download_file_function,
            css_id, ignore_anchor_value_list=[]):
  os.makedirs(save_directory, exist_ok=True)
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  # Find the specific section with css id
  target_section = soup.find(id=css_id)
  if not target_section:
    print(f"Error: No section with id '{css_id}' found in {url}")
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
                download_file_function, css_id, ignore_anchor_value_list)
    else:
      # It's a file link, check extension and download if valid
      file_url = urljoin(url, href)
      if (download_file_function is not None and
          is_file(file_url)):
        download_file_function(file_url, save_directory)

def is_file(url):
  try:
    response = requests.head(url, allow_redirects=True)
    content_type = response.headers.get('Content-Type')

    # Check the Content-Type header
    if content_type:
      if 'text/html' not in content_type:
        return True
    if content_type is None:
      return True

    # Check the file extension in the URL
    url_path = os.path.basename(url)
    mime_type, _ = mimetypes.guess_type(url_path)
    print(f"{url=} || {mime_type=}")
    print("-"*40)
    if mime_type and not mime_type.startswith('text/html'):
      return True
    if mime_type is None:
      return True

    # # If HEAD request doesn't provide enough info, perform a GET request
    # response = requests.get(url)
    # if response.headers.get('Content-Type'):
    #   content_type = response.headers.get('Content-Type')
    #   if content_type and 'text/html' not in content_type:
    #     return True

    return False
  except requests.RequestException as e:
    print(f"An error occurred: {e}")
    return False
