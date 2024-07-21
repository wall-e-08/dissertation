import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumScraper:
  def __init__(self, url, headless=True):
    self.url = url
    self.driver = self.init_driver(headless)

  @staticmethod
  def init_driver(headless):
    chrome_options = Options()
    if headless:
      chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument(
      "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

  def human_like_scroll(self, speed):
    last_height = self.driver.execute_script("return document.body.scrollHeight")
    while True:
      self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(speed * random.random())
      new_height = self.driver.execute_script("return document.body.scrollHeight")
      if new_height == last_height:
        break
      last_height = new_height

  def scrape(self):
    self.driver.get(self.url)
    time.sleep(2)  # Wait for the page to load completely
    self.human_like_scroll(speed=2)
    html = self.driver.page_source
    self.driver.quit()
    return html