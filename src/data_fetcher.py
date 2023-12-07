from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import numpy as np
import pyautogui
from PIL import Image
import uuid 
import os


class DataFetcher:
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options)        
        self.numbersAndLocationExistanceArray = np.zeros((10, 4))
        self.digitsImagesCounterDictionary = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
        self.tabsAndNumbersDictionary = {}
        self.originalTab = 0


    def createDatabase(self):
        self.fillDataAndSubmit()
        self.originalTab = self.driver.current_window_handle
        for i in range(10):
            number, imageURL = self.getURLAndStringOfNumberDisplayed()
            self.createNewTab(imageURL)
            currentTab = self.driver.current_window_handle
            self.tabsAndNumbersDictionary[currentTab] = number
            self.switchToMainTab()
            time.sleep(1)
            self.refreshNumber()
        self.createDatabaseFromOpenTabs()
            
        # self.createNumbersAndURLsDictionary()
        # time.sleep(5)
        # self.createDatabaseFromDictionary()
        self.driver.close()
    
    # def createDatabaseFromDictionary(self):
    #     for number, url in self.numbersAndURLToFetch.items():
    #         for i in range(10):
    #             self.saveImagesOfSpecificNumber(url, number)

    def switchToMainTab(self):
        for window_handle in self.driver.window_handles:
            if window_handle != self.originalTab:
                self.driver.switch_to.window(window_handle)
                break
    
    def createNewTab(self, imageURL):
        self.driver.switch_to.new_window('tab')
        self.driver.get(imageURL)
    
    def getURLAndStringOfNumberDisplayed(self):
        numbersImage = self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_RadCaptcha1_CaptchaImageUP"]')
        imageURL = numbersImage.get_attribute("src")
        number = input('What is the displayed number?')
        self.driver.switch_to.new_window('tab')
        self.driver.get(imageURL)
        return number, imageURL
    
    def createDatabaseFromOpenTabs(self):
        return
    
    def fillDataAndSubmit(self):
        self.driver.get("https://nadlan.taxes.gov.il/svinfonadlan2010/startpageNadlanNewDesign.aspx?ProcessKey=cb2fc2f5-08db-4099-9d1e-8eb9f6bcda42")
        cityInput, propertyType, transactionType, submitButton = self.getElementsFromNadlanWebsite()
        cityInput.send_keys("חיפה")
        propertyTypeSelect = Select(propertyType)
        propertyTypeSelect.select_by_index(1)
        time.sleep(5)
        transactionTypeSelect = Select(transactionType)
        transactionTypeSelect.select_by_index(2)
        submitButton.click()
        time.sleep(5)


    def getElementsFromNadlanWebsite(self):
        cityInput = self.driver.find_element(By.XPATH, '//*[@id="txtYeshuv"]')
        propertyType =  self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_DDLTypeNehes"]')
        transactionType = self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_DDLMahutIska"]')
        submitButton = self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_btnHipus"]')
        return cityInput, propertyType, transactionType, submitButton

    # def createNumbersAndURLsDictionary(self):
    #     for i in range(1):
    #         numbersImage = self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_RadCaptcha1_CaptchaImageUP"]')
    #         imageURL = numbersImage.get_attribute("src")
    #         displayedNumber = input('What is the displayed number?')
    #         self.driver.switch_to.new_window('tab')
    #         self.driver.get("https://nadlan.taxes.gov.il/svinfonadlan2010/startpageNadlanNewDesign.aspx?ProcessKey=cb2fc2f5-08db-4099-9d1e-8eb9f6bcda42")
    #         self.numbersAndURLToFetch[displayedNumber] = imageURL
            # self.refreshNumber()
            
        
    def refreshNumber(self):
        refreshLink = self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_RadCaptcha1_CaptchaLinkButton"]')
        refreshLink.click()

    def saveImagesOfSpecificNumber(self, imageURL, number):
        self.driver.get(imageURL)
        myScreenshot = pyautogui.screenshot(region=(806, 614, 180, 48))
        imagePath = f'/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/Data/{number}.png'
        myScreenshot.save(imagePath)
        self.splitImageToFourDigits(imagePath, number)
        os.remove(imagePath)
        time.sleep(2)


    def splitImageToFourDigits(self, imagePath, number):
        with Image.open(imagePath) as image:
            firstDigitRight = image.width / 4
            secondDigitRight = image.width / 2
            thirdDigitRight = image.width * 3 / 4

            firstDigit = int(number[0])
            secondDigit = int(number[1])
            thirdDigit = int(number[2])
            fourthDigit = int(number[3])

            if(self.digitsImagesCounterDictionary[firstDigit] <= 10000):
                firstCroppedImage = image.crop((0, 0, firstDigitRight, image.height))
                firstCroppedImage.save(f'/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/Data/{firstDigit}_{uuid.uuid4()}.png')
                self.digitsImagesCounterDictionary[firstDigit] += 1

            if(self.digitsImagesCounterDictionary[secondDigit] <= 10000):
                secondCroppedImage = image.crop((firstDigitRight, 0, secondDigitRight, image.height))
                
                secondCroppedImage.save(f'/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/Data/{secondDigit}_{uuid.uuid4()}.png')
                self.digitsImagesCounterDictionary[secondDigit] += 1

            if(self.digitsImagesCounterDictionary[thirdDigit] <= 10000):
                thirdCroppedImage = image.crop((secondDigitRight, 0, thirdDigitRight, image.height))
                thirdCroppedImage.save(f'/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/Data/{thirdDigit}_{uuid.uuid4()}.png')
                self.digitsImagesCounterDictionary[thirdDigit] += 1

            if(self.digitsImagesCounterDictionary[fourthDigit] <= 10000):
                fourthCroppedImage = image.crop((thirdDigitRight, 0, image.width, image.height))
                fourthCroppedImage.save(f'/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/Data/{fourthDigit}_{uuid.uuid4()}.png')
                self.digitsImagesCounterDictionary[fourthDigit] += 1
            

    # def deleteImage(self, imageToDelete):

        

        








