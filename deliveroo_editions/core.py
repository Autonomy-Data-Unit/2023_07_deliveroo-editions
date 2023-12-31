# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_deliveroo.ipynb.

# %% auto 0
__all__ = ['initialise_driver', 'get_yearly_captures', 'add_restaurants', 'get_metadata', 'add_metadata_to_dataset',
           'get_element_by_id']

# %% ../nbs/01_deliveroo.ipynb 2
def initialise_driver(service, # Instance of `selenium.webdriver.chrome.service.Service`
                      headless:bool=False): # Set browser to run headless [False] or visble [True]
    "Initialises Chrome WebDriver"
    options = Options()
    options.headless = headless
    return webdriver.Chrome(service=service, options=options) 

def get_yearly_captures(year, url):
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    year_selector = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sparkline-year-label')))
    year_selector = driver.find_element(By.XPATH, f'//*[contains(@class, "sparkline-year-label") and text()="{year}"]')
    year_selector.click()
    wait = WebDriverWait(driver, 10)  # Maximum wait time in seconds
    calendar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "calendar-grid")))
    captures = calendar.find_elements(By.CSS_SELECTOR, 'a')
    area_urls = []
    for capture in captures:
        area_urls.append(capture.get_attribute('href'))
    return area_urls

def add_restaurants(dataset, area_url):
    driver.get(area_url)
    wait = WebDriverWait(driver, 20)  # Maximum wait time in seconds
    ul_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[class*="HomeFeedGrid"]')))
    soup = BeautifulSoup(ul_element.get_attribute('innerHTML'), 'html.parser')
    filtered_li_tags = [li for li in soup.find_all('li') if not li.find_parents('li')]
    for tag in filtered_li_tags:
        metadata = get_metadata(tag)
        if metadata:
            dataset = add_metadata_to_dataset(dataset, metadata, area_url)
    return dataset
    
def get_metadata(tag):
#         list_items = tag.find_all('ul')[0].find_all('li')
        list_sections = tag.find_all('ul')
        if list_sections:
            # find the section with 3 or more items in its list
            for list_section in list_sections:
                list_items = list_section.find_all('li')
                if len(list_items) >= 3: 
                    name = list_items[0].text
                    try:
                        restaurant_url = tag.find_all('a')[0]['href']
                        location = restaurant_url.split("/")[5]
        #                     distance = list_items[2].find_all('span')[0].text
                        return {'name': name, 'restaurant_url': restaurant_url, 'location': location}
#                     return {'name': name, 'restaurant_url': restaurant_url, 'location': location, 'distance': distance}
                    except:
                        print(f"Couldn't get metadata for {name}")
                        return
                else:
                    pass
            return
        else:
            return
        
def add_metadata_to_dataset(dataset, metadata, area_url):
    location = metadata['location']
    name = metadata['name']
    restaurant_url = metadata['restaurant_url']
#     distance = metadata['distance']
    timestamp = area_url.split('/')[4]
    if location not in dataset:
        dataset[location] = {}
    if name not in editions[location]: 
        dataset[location][name] = {}
        dataset[location][name]["timestamps"] = []
        dataset[location][name]["restaurant_url"] = restaurant_url
        dataset[location][name]["timestamp_urls"] = []
#         dataset[location][name]["distances"] = []
    if timestamp not in dataset[location][name]["timestamps"]:
        dataset[location][name]["timestamps"].append(timestamp)
    if area_url not in dataset[location][name]["timestamp_urls"]:
        dataset[location][name]["timestamp_urls"].append(area_url)
#     if distance not in dataset[location][name]["distances"]:
#         dataset[location][name]["distances"].append(distance)
    return dataset

def get_element_by_id(url:str, # url to search for
                driver, # driver initialised with `initialise_driver`
                id:str, # id of element to wait for when url page renders
                timeout:int=15, # seconds to wait for element to appear before timeout error
               ):
                   "Gets selenium web element that matches HTML element ID. Waits for element to load before user-defined timeout"
                   driver.get(base_url)
                   wait = WebDriverWait(driver, timeout)
                   filter_input = wait.until(EC.presence_of_element_located((By.ID, 'resultsUrl_filter')))
                   
                   return filter_input
