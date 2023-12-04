from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import numpy as np
import pyautogui

class DataFetcher:
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options)        
        self.numbersAndLocationExistanceArray = np.zeros((10, 4))

    def fillDataAndSubmit(self):
        self.driver.get("https://nadlan.taxes.gov.il/svinfonadlan2010/startpageNadlanNewDesign.aspx?ProcessKey=cb2fc2f5-08db-4099-9d1e-8eb9f6bcda42")

        cityInput = self.driver.find_element(By.XPATH, '//*[@id="txtYeshuv"]')
        cityInput.send_keys("חיפה")

        propertyTipe =  self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_DDLTypeNehes"]')
        propertyTypeSelect = Select(propertyTipe)
        propertyTypeSelect.select_by_index(1)
        
        time.sleep(5)
        transactionType = self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_DDLMahutIska"]')
        transactionTypeSelect = Select(transactionType)
        transactionTypeSelect.select_by_index(2)

        submitButton = self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_btnHipus"]')
        submitButton.click()

        time.sleep(5)

        numbersImage = self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_RadCaptcha1_CaptchaImageUP"]')
        imageURL = numbersImage.get_attribute("src")
        displayedNumber = input('What is the displayed number?')
        for i in range(20):
            self.saveImages(imageURL, i, displayedNumber)
            time.sleep(3)
        
        self.driver.close()

    def saveImages(self, imageURL, index, displayedNumber):
        self.driver.get(imageURL)
        myScreenshot = pyautogui.screenshot(region=(806, 614, 180, 48))
        myScreenshot.save(f'/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/Data/{displayedNumber}_{index}.png')
        








