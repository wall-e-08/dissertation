import re


def get_date_from_swlive_website(url):
  date_pattern = r'/(\d{4})/(\d{2})/(\d{2})/\w+\.html'
  match = re.search(date_pattern, url)

  if match:
    year, month, day = match.groups()
    return f"{year}-{month}-{day}"

  return None

