import os
import requests
from urllib.parse import urlparse
from download_from_url.file import from_url


URL = "https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-indices/"
IGNORE_VALUE_LIST_LOWERCASE = [None, "name", "last modified", "size", "parent directory", "nesdis",
                            "home", "privacy policy", "questions", "us department of commerce", 'noaa']
CSS_ID = "main_text"


def download_file(url, save_path):
  # Extract filename from URL
  parsed_url = urlparse(url)
  filename = os.path.basename(parsed_url.path)

  # Ensure the save path is not a directory or if the file already exists
  _file_path = os.path.join(save_path, filename)
  if os.path.isdir(_file_path) or os.path.exists(_file_path):
    print(f"Skipping: {_file_path}")
    return

  # Download file
  response = requests.get(url)

  # Save file to disk
  with open(_file_path, 'wb') as f:
    f.write(response.content)

  print(f"Downloading {filename}...")

if __name__ == '__main__':
  file_path = os.path.dirname( __file__ )
  base_url_path = urlparse(URL).path
  from_url(URL, os.path.abspath(os.path.join(file_path, '..', "data")), base_url_path,
          download_file, CSS_ID, IGNORE_VALUE_LIST_LOWERCASE)
