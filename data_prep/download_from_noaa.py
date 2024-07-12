import os
from urllib.parse import urlparse
from download.file import from_url


URL = "https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-indices/"
IGNORE_VALUE_LIST_LOWERCASE = [None, "name", "last modified", "size", "parent directory", "nesdis",
                            "home", "privacy policy", "questions", "us department of commerce", 'noaa']
CSS_ID = "main_text"


if __name__ == '__main__':
  file_path = os.path.dirname( __file__ )
  base_url_path = urlparse(URL).path
  from_url(URL, os.path.abspath(os.path.join(file_path, '..', "data")), base_url_path,
           {"id": CSS_ID}, IGNORE_VALUE_LIST_LOWERCASE)
