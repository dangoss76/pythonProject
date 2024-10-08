import pytest

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd
@pytest.mark.usefixtures("setup")

class TestQuotesDropdown:
    def test_quotes_dropdown(self):
        record_property("testrail_result_comment", "1. test the quotes dropdown")
        # Navigate to TMX
        self.driver.get("https://www.m-x.ca/en/trading/data/quotes")

        # Defining the columns to read
        quoteOptions = ['symbolOEQ', 'symbolETF', 'symbolSSF']  # Select name
        quoteCSV = ['tests/csv/equity.csv', 'tests/csv/etf.csv', 'tests/csv/shareFutures.csv']  # CSV fie

        for q1, q2 in zip(quoteOptions, quoteCSV):

            data = pd.read_csv(f'{q2}')

            for index, row in data.iterrows():
                element = self.driver.find_element(By.ID,'page-content') # Find the top element of the page
                self.driver.execute_script("arguments[0].scrollIntoView();", element) # We scroll back to top
                #self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
                dropdown_equity = self.driver.find_element(By.ID, (f'{q1}'))  # we select a quotes in the dropdown
                select = Select(dropdown_equity)
                select.select_by_value(row['symbol'])

                clickOkBtn = self.driver.find_element(By.XPATH,
                                                  "//select[@id='" + f'{q1}' + "']/following-sibling::div").click()  # Click OK button next to the select

                quoteResult = self.driver.find_element(By.TAG_NAME, 'h2').text  # Validate if title match
                assert quoteResult == row['title']

                print(row['symbol'], row['title'])

        print("Test Execution Successfully Completed!")
