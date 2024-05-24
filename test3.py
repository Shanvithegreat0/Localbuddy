from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
import time

# Path to your ChromeDriver
chrome_driver_path = 'C:/Users/HARI OM/Desktop/chromedriver-win64/chromedriver-win64/chromedriver.exe'

# Initialize ChromeDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Define the URL of the target website (for example, Google Maps)
url = "https://www.google.com/maps"

# Open the URL
driver.get(url)
time.sleep(2)  # Allow time for the page to load

# Find the search input element on Google Maps
search_box = driver.find_element(By.XPATH, "//input[@id='searchboxinput']")

# Enter the text into the search box and submit
place_type = "park"
query = place_type + " in Jankipuram"
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)
time.sleep(5)  # Allow time for search results to load

# Start iterating from the first odd-numbered element
index = 3

# Initialize list to store data
data_list = []

while True:
    try:
        # Construct XPath for the odd-numbered elements
        xpath = f"//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{index}]/div/a"

        # //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/a for hotel
        # //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[3]/div/a for hospital

        place_element = driver.find_element(By.XPATH, xpath)
        
        # Click on the element
        place_element.click()
        time.sleep(3)  # Allow time for the place details to load
        
        # Get the place name
        place_name = driver.find_element(By.XPATH, "//*[@id='QA0Szd']/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1").text
        
        # Click on the reviews button if available
        try:
            reviews_button = driver.find_element(By.XPATH, "//*[@id='QA0Szd']/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[3]/div/div/button[2]/div[2]/div[2]")
        
            # //*[@id='QA0Szd']/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[3]/div/div/button[2]/div[2]/div[2] for hospital
            # //*[@id='QA0Szd']/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[3]/div/div/button[3]/div[2]/div[2] for hotel


            reviews_button.click()
            time.sleep(1)  # Allow time for the reviews to load

            # Scroll within the reviews container to load all reviews
            reviews_container = driver.find_element(By.XPATH, "//*[@id='QA0Szd']/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]")
            for _ in range(10):  # Adjust the range to scroll enough times to load all reviews
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", reviews_container)
                time.sleep(1)  # Allow time for scrolling

            # Get the page source and parse with BeautifulSoup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Extract reviews
            reviews = soup.find_all('span', class_='wiI7pd')  # Adjust class name as needed
        except:
            reviews = []

        # Create dictionary to store data
        place_data = {
            "place": place_name,
            "reviews": [review.text.strip() for review in reviews]
        }

        # Append data to list
        data_list.append(place_data)
        
        # Write data to JSON file after scraping each place
        with open(place_type +'.json', 'w', encoding='utf-8') as json_file:
            json.dump(data_list, json_file, indent=4, ensure_ascii=False)
        
        # Move to the next place
        index += 2
    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Close the browser
driver.quit()
