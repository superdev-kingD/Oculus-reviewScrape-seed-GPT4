import os, os.path
import pandas as pd
# import json
from bs4 import BeautifulSoup as BS
from google.oauth2 import service_account
# import pygsheets as pygsheets
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(
    level=logging.DEBUG,
    filename='LightSport.log',
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class PowerBeatsVR:
    def run_browser(self, url):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.maximize_window()
        self.browser.get(url)

    def collect_reviews(self):
        self.run_browser('https://www.oculus.com/experiences/quest/4336749139724039/')
        time.sleep(1)

        # Get total page count
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='app-review-pager__number']")))
        pageCount = self.browser.find_elements(By.XPATH, "//div[@class='app-review-pager__number']")[1].text
        print(f"total page count: {pageCount}")

        # Review container
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='app-review']")))
        names = []
        dates = []
        ratings = []
        titles = []
        descriptions = []
        for i in range(int(pageCount)):
            print(f"Page number: {i+1}")
            time.sleep(5)
            reviewContainers = self.browser.find_elements(By.XPATH, "//div[@class='app-review']")
            for reviewContainer in reviewContainers:
                name = reviewContainer.find_element(By.XPATH, ".//h1[@class='bxHeading bxHeading--level-5 app-review__author']").text
                names.append(name)
                date = reviewContainer.find_element(By.XPATH, ".//div[@class='app-review__date']").text
                dates.append(date)
                rating = len(reviewContainer.find_elements(By.XPATH, ".//div[@class='app-review__star-container']/div[@class='app-review__stars bxStars--spacing-0']/i[@class='bxStars bxStars--white']"))
                ratings.append(rating)
                title = reviewContainer.find_element(By.XPATH, ".//h1[@class='bxHeading bxHeading--level-5 app-review__title']").text
                titles.append(title)
                description = reviewContainer.find_element(By.XPATH, ".//div[@class='clamped-description__content']").text
                descriptions.append(description)
                print(f"{name} | {date} | {title}")
            # page next
            nextButton = self.browser.find_elements(By.XPATH, "//button[@data-testid='store:pdp:review-pager:next']")[1]
            nextButton.click()

        # Export result into CSV file
        dict = {'Name': names, 'Date': dates, 'Star Rating': ratings, 'Title': titles, 'Feedback': descriptions}  
        df = pd.DataFrame(dict) 
        # saving the dataframe 
        df.to_csv('PowerBeatsVR_Reviews.csv')

if __name__ == "__main__":
    PowerBeatsVR = PowerBeatsVR()
    PowerBeatsVR.collect_reviews()