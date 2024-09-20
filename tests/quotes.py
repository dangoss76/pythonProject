import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import pandas as pd
import csv
import time

@pytest.fixture()
def setup(request):
    chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())

    chrome_options = Options()
    options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
    for option in options:
        chrome_options.add_argument(option)

    request.cls.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


    yield request.cls.driver
    request.cls.driver.close()

print("Test Execution Started")

@pytest.mark.usefixtures("setup")
class TestExampleOne:
    def test_title(self):

# browser = webdriver.Firefox()

        # Navigate to TMX
        self.driver.get("https://www.m-x.ca/en/trading/data/quotes")

        # Defining the columns to read
        quoteOptions = ['symbolOEQ', 'symbolETF', 'symbolSSF']  # Select name
        quoteCSV = ['equity.csv', 'etf.csv', 'shareFutures.csv']  # CSV fie

        for q1, q2 in zip(quoteOptions, quoteCSV):

            data = pd.read_csv(f'{q2}')

            for index, row in data.iterrows():
                # element = browser.find_element(By.ID,'page-content') # Find the top element of the page
                # browser.execute_script("arguments[0].scrollIntoView();", element) # We scroll back to top
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
                dropdown_equity = self.driver.find_element(By.ID, (f'{q1}'))  # we select a quotes in the dropdown
                select = Select(dropdown_equity)
                select.select_by_value(row['symbol'])

                clickOkBtn = self.driver.find_element(By.XPATH,
                                                  "//select[@id='" + f'{q1}' + "']/following-sibling::div").click()  # Click OK button next to the select

                quoteResult = self.driver.find_element(By.TAG_NAME, 'h2').text  # Validate if title match
                assert quoteResult == row['title']

                print(row['symbol'], row['title'])

        browser.quit()
        print("Test Execution Successfully Completed!")
