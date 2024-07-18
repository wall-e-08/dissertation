import os
from random import random
from urllib.parse import urlparse
from download.file import from_url

URL = "http://jsoc.stanford.edu/data/hmi/images/"
IGNORE_VALUE_LIST_LOWERCASE = [None, "name", "last modified", "size", "parent directory",
                               "description", "latest", "b96m", "ccmc"]

def file_filter(url):
  if url is not None and url.endswith((
      "000000_Ic_512.jpg", "000000_Ic_flat_512.jpg", "000000_M_512.jpg", "000000_M_color_512.jpg"
  )):
    return True

  return False

if __name__ == '__main__':
  # get_date_range_arr()
  file_path = os.path.dirname( __file__ )
  dir_path = os.path.abspath(os.path.join(file_path, '..', "data", "jsoc", "images"))
  base_url_path = urlparse(URL).path

  rand_id = str(random()).replace('0.', '')
  url_filename = os.path.join(dir_path, f"{rand_id}.txt")

  with open(url_filename, 'w') as url_file:
    url_file.write(f"{URL}\n\n")
  from_url(URL, dir_path, base_url_path, url_filename,
           {"name": "table"}, IGNORE_VALUE_LIST_LOWERCASE, file_filter)

