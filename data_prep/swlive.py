from celery import group

from download.task import scrape_xray_page, scrape_dayobs_page
from utils.datetime import get_date_from_swlive_website
from utils.url import generate_urls


def create_grouped_tasks(start_date, end_date):
  tasks = []
  urls = generate_urls(start_date, end_date)

  for xray_url, dayobs_url in urls:
    tasks.append(scrape_xray_page.s(xray_url, get_date_from_swlive_website(xray_url)))
    tasks.append(scrape_dayobs_page.s(dayobs_url, get_date_from_swlive_website(dayobs_url)))

  grouped_tasks = group(tasks)
  return grouped_tasks


if __name__ == "__main__":
  start_date = '1996-06-01'
  end_date = '2024-06-30'
  result = create_grouped_tasks(start_date, end_date).apply_async()
  print("Task submitted. Waiting for result...")
