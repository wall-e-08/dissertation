import os
import pandas as pd
import requests

from bs4 import BeautifulSoup
from celery_app import app, CallbackTask
from download.selenium_scrapper import SeleniumScraper
from urllib.parse import urlparse

from utils.write_read import append_to_csv


@app.task(base=CallbackTask, default_retry_delay=1 * 60) # retry after 1min
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


@app.task(base=CallbackTask, default_retry_delay=1 * 60)
def scrape_xray_page(url, date):
  try:
    scraper = SeleniumScraper(url)
    html = scraper.scrape()

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.select_one('#Archive_SolarFlare_table table.table.table-sm.table-striped')

    data = []
    rows = table.find_all('tr')[1:]  # Skip the header row
    for row in rows:
      cols = row.find_all('td')
      if cols[0].text == 'None':
        continue

      flux = cols[1]
      if len(flux.contents) > 0:
        flux = flux.contents[0].text.strip()
      else:
        flux = None

      data.append({
        'Date': date,
        'Region': cols[0].text.strip(),
        'Flux': flux,
        'Start': cols[2].text.strip(),
        'Maximum': cols[3].text.strip(),
        'End': cols[4].text.strip()
      })

    append_to_csv(data, ['Date', 'Region', 'Flux', 'Start', 'Maximum', 'End'], 'xray.csv')
    with open("xray.txt", "a") as file:
      file.write(f"{data}\n")
  except Exception as e:
    print(e)
    with open("xray_err.txt", "a") as file:
      file.write(f"{url}: {e}\n")

@app.task(base=CallbackTask, default_retry_delay=1 * 60)
def scrape_dayobs_page(url, date):
  try:
    scraper = SeleniumScraper(url)
    html = scraper.scrape()

    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all('table', {'id': True})

    data = []
    for table in tables:
      region_tags = table.select('tr th h3')
      if len(region_tags) > 0 and len(region_tags[0].contents) > 0:
        region = region_tags[0].contents[0].text.strip().replace("Region ", "")
      else:
        region = ""

      row = table.find('tbody')

      cols = row.find_all('td')

      sunspot_num = cols[0]
      if len(sunspot_num.contents) > 0:
        sunspot_num = sunspot_num.contents[0].text.strip()
      else:
        sunspot_num = None

      size = cols[1]
      if len(size.contents) > 0:
        size = size.contents[0].text.strip()
      else:
        size = None

      mag_css = cols[2].find('i').get('class')
      if mag_css and len(mag_css) > 0:
        mag_class = " ".join(mag_css)
      else:
        mag_class = None

      data.append({
        'Date': date,
        'Region': region,
        'Sunspot Number': sunspot_num,
        'Size': size,
        'Magnetic Classification': mag_class,
        'Sunspot Classification': cols[3].text.strip(),
        'Location': cols[4].text.strip(),
      })

    append_to_csv(data, ['Date', 'Region', 'Sunspot Number', 'Size', 'Magnetic Classification',
                         'Sunspot Classification', 'Location'], 'dayobs.csv')

    with open("dayobs.txt", "a") as file:
      file.write(f"{data}\n")
  except Exception as e:
    print(e)
    with open("dayobs_err.txt", "a") as file:
      file.write(f"{url}: {e}\n")



# @app.task(name='download.task.scrap_swlive', default_retry_delay=1 * 60)
# def scrap_swlive(start_date, end_date):
#   urls = generate_urls(start_date, end_date)
#
#   xray_tasks = group(scrape_xray_page.s(xray_url) for xray_url, _ in urls)()
#   dayobs_tasks = group(scrape_dayobs_page.s(dayobs_url) for _, dayobs_url in urls)()
#
#   xray_results = xray_tasks.get()
#   dayobs_results = dayobs_tasks.get()
#
#   xray_data = [item for sublist in xray_results for item in sublist]
#   dayobs_data = [item for sublist in dayobs_results for item in sublist]
#
#   xray_df = pd.DataFrame(xray_data)
#   dayobs_df = pd.DataFrame(dayobs_data)
#
#   xray_csv = 'xray_data.csv'
#   dayobs_csv = 'dayobs_data.csv'
#
#   xray_df.to_csv(xray_csv, index=False)
#   dayobs_df.to_csv(dayobs_csv, index=False)
#
#   return {'xray_csv': xray_csv, 'dayobs_csv': dayobs_csv}