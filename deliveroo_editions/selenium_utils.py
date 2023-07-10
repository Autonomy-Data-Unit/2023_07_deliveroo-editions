# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/selenium_utils.ipynb.

# %% auto 0
__all__ = ['headers', 'service', 'driver', 'initialise_driver', 'get_element_by']

# %% ../nbs/selenium_utils.ipynb 2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# %% ../nbs/selenium_utils.ipynb 4
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

# %% ../nbs/selenium_utils.ipynb 6
service = Service(executable_path=ChromeDriverManager().install())

# %% ../nbs/selenium_utils.ipynb 7
assert service

# %% ../nbs/selenium_utils.ipynb 8
def initialise_driver(service, # Instance of `selenium.webdriver.chrome.service.Service`
                      headless:bool=False): # Set browser to run headless [False] or visble [True]
    "Initialises Chrome WebDriver"
    options = Options()
    options.headless = headless
    return webdriver.Chrome(service=service, options=options) 

driver = initialise_driver(service, True)

# %% ../nbs/selenium_utils.ipynb 9
assert driver

# %% ../nbs/selenium_utils.ipynb 12
def get_element_by(url:str, # url to search for
                       driver, # driver initialised with `initialise_driver`
                       css_component:str="id", # accepted values: `id`, `class_name`, `css_selector`
                       css_component_value:str="", # id of element to wait for when url page renders
                       timeout:int=15, # seconds to wait for element to appear before timeout error
                      ):
                   "Gets selenium web element that matches HTML element ID. Waits for element to load before user-defined timeout"
                   css_component_lookup = {"id": By.ID, "css_selector": By.CSS_SELECTOR, "class_name": By.CLASS_NAME}
                   if not css_component_lookup[css_component]:
                       print("Invalid css_component provided. Should be either 'id', 'class_name' or 'css_selector")
                       return
                   driver.get(url)
                   wait = WebDriverWait(driver, timeout)    
                   filter_input = wait.until(EC.presence_of_element_located((css_component_lookup[css_component], css_component_value)))
                   return filter_input
