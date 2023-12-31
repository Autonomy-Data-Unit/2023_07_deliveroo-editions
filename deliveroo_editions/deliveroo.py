# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/001_deliveroo.ipynb.

# %% auto 0
__all__ = ['tags', 'get_restaurant_tags', 'get_timestamp', 'get_restaurants']

# %% ../nbs/001_deliveroo.ipynb 2
from .selenium_utils import *
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from bs4 import BeautifulSoup
from ratelimit import limits, RateLimitException, sleep_and_retry
import time

# %% ../nbs/001_deliveroo.ipynb 3
@sleep_and_retry
@limits(calls=1, period=20)
def get_restaurant_tags(url:str, # URL for Deliveroo restaurants page
                        driver=None
                       ):
    "Returns all list elements from Deliveroo restaurants webpage corresponding to a restaurant"
    if not driver:
        driver = initialise_driver(service,True)
    time.sleep(1)
    driver.get(url)
    wait = WebDriverWait(driver, 10)  # Maximum wait time in seconds
    ul_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[class*="HomeFeedGrid"]')))
    soup = BeautifulSoup(ul_element.get_attribute('innerHTML'), 'html.parser')
    filtered_li_tags = [li for li in soup.find_all('li') if not li.find_parents('li')]
    return filtered_li_tags

tags = get_restaurant_tags("https://web.archive.org/web/20201019/https://deliveroo.co.uk/restaurants/brighton/brighton-editions?tags=deliveroo+editions")
assert len(tags) == 13

# %% ../nbs/001_deliveroo.ipynb 4
def get_timestamp(url:str # URL for Deliveroo
                 ):
                     "Returns YYYYMMDD timestamp from url of format: https://web.archive.org/web/YYYYMMDD/"
                     timestamp = url.split('/')[4]
                     if timestamp.isdigit():
                         return timestamp[0:8]
                     else:
                         print("Could not extract timestamp of format YYYYMMDD from url provided")
                         return

assert get_timestamp("https://web.archive.org/web/20201019/https://deliveroo.co.uk/restaurants/brighton/brighton-editions?tags=deliveroo+editions")

# %% ../nbs/001_deliveroo.ipynb 5
def get_restaurants(url:str, # URL for Deliveroo restaurants page
                    # headless:bool=True,
                    driver= None
                   ): # run headless (True) or with browser (False).
                       """Gets the restaurant `name`, editions `location` and Deliveroo `restaurant_url`
                       for each restaurant on url page."""
                       if not driver:
                           driver = initialise_driver(service,True)
                       restaurants = []
                       tags = get_restaurant_tags(url, driver)
                       timestamp = get_timestamp(url)
                       for tag in tags:
                           name, restaurant_url, location = "", "", ""
                           list_sections = tag.find_all('ul')
                           if list_sections:
                               for list_section in list_sections:
                                   list_items = list_section.find_all('li')
                                   if len(list_items) >= 3:
                                       name = list_items[0].text
                                       try:
                                           restaurant_url = tag.find_all('a')[0]['href']
                                           location = restaurant_url.split("/")[5]
                                       except Exception as e: 
                                           print(e)
                                           print(f"Couldn't get metadata for {name} in {url}")
                                       restaurants.append({'name': name, 'location': location, 'timestamp': timestamp, 'restaurant_url': restaurant_url, 'timestamp_url': url})
                                   else:
                                       pass
                           else:
                               print(f"No restaurants found at {url}")
                       return restaurants
