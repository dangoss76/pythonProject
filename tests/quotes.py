import pytest
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

#Fixture for Chrome
@pytest.fixture(scope="class")
def chrome_driver_init(request):
    chrome_driver = webdriver.Chrome()
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()

@pytest.mark.usefixtures("chrome_driver_init")
class TestQuote:
    def testQuote(self):

        print("Test Execution Started")

        #options = webdriver.ChromeOptions()
        #options.add_argument('--ignore-ssl-errors=yes')
        #options.add_argument('--ignore-certificate-errors')
        #options.add_argument("--headless=new")  # for Chrome >= 109

       # self.browser = webdriver.Remote(
           # command_executor='http://localhost:4444/wd/hub',
           # options=options
        #)

        # Open Browser
        # browser = webdriver.Firefox()

        # Navigate to TMX
        self.browser.get("https://www.m-x.ca/en/trading/data/quotes")

        # Defining the columns to read
        quoteOptions = ['symbolOEQ', 'symbolETF', 'symbolSSF']  # Select name
        quoteCSV = ['csv/equity.csv', 'csv/etf.csv', 'csv/shareFutures.csv']  # CSV fie

        for q1, q2 in zip(quoteOptions, quoteCSV):

            data = pd.read_csv(f'{q2}')

            for index, row in data.iterrows():
                # element = browser.find_element(By.ID,'page-content') # Find the top element of the page
                # browser.execute_script("arguments[0].scrollIntoView();", element) # We scroll back to top
                self.browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
                dropdown_equity = self.browser.find_element(By.ID, (f'{q1}'))  # we select a quotes in the dropdown
                select = Select(dropdown_equity)
                select.select_by_value(row['symbol'])

                clickOkBtn = self.browser.find_element(By.XPATH,
                                                  "//select[@id='" + f'{q1}' + "']/following-sibling::div").click()  # Click OK button next to the select

                quoteResult = self.browser.find_element(By.TAG_NAME, 'h2').text  # Validate if title match
                assert quoteResult == row['title']

                print(row['symbol'], row['title'])

        self.browser.quit()
        print("Test Execution Successfully Complpeted!")