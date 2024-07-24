import re

import pandas as pd


def generate_urls(start_date, end_date):
  base_url_xray = "https://www.spaceweatherlive.com/en/archive/{}/xray.html"
  base_url_dayobs = "https://www.spaceweatherlive.com/en/archive/{}/dayobs.html"
  date_list = pd.date_range(start=start_date, end=end_date)
  urls = [(base_url_xray.format(date.strftime('%Y/%m/%d')), base_url_dayobs.format(date.strftime('%Y/%m/%d'))) for date
          in date_list]
  return urls

def region_from_url(url):
  match = re.search(r'(\d+)\.html', url)
  if match:
    return match.group(1)
  else:
    return None