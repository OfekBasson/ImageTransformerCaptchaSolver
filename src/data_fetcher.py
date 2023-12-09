from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import numpy as np
import pyautogui
from PIL import Image
import uuid 
import os
import pandas as pd
import csv


class DataFetcher:
    
    def __init__(self):
        self.csvFileName = 'digits_images_counter.csv'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.numbersAndLocationExistanceArray = np.zeros((10, 4))
        self.digitsImagesCounterDataFrame = self.getUpdatedDigitsImagesCounterDataFrame()
        self.tabsAndNumbersDictionary = {}

    def createDatabase(self):
        for i in range(3):
            self.fillDataAndSubmit()
            number, imageURL = self.getURLAndStringOfNumberDisplayed()
            self.createNewTab(imageURL)
            self.saveImagesOfSpecificNumber(imageURL, number)
            self.driver.close()
    
    def createNewTab(self, imageURL):
        self.driver.switch_to.new_window('tab')
        self.driver.get(imageURL)
    
    def getURLAndStringOfNumberDisplayed(self):
        numbersImage = self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_RadCaptcha1_CaptchaImageUP"]')
        imageURL = numbersImage.get_attribute("src")
        number = input('What is the displayed number?')
        return number, imageURL
    
    def fillDataAndSubmit(self):
        self.driver = webdriver.Chrome(self.options)        
        self.originalTab = self.driver.current_window_handle
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
            
        
    def refreshNumber(self):
        refreshLink = self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_RadCaptcha1_CaptchaLinkButton"]')
        refreshLink.click()

    def saveImagesOfSpecificNumber(self, imageURL, number):
        for i in range(3):
            self.driver.get(imageURL)
            myScreenshot = pyautogui.screenshot(region=(806, 614, 180, 48))
            imagePath = f'/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/Data/{number}.png'
            myScreenshot.save(imagePath)
            self.splitImageToFourDigits(imagePath, number)
            os.remove(imagePath)
            time.sleep(2)
        self.digitsImagesCounterDataFrame.to_csv(self.csvFileName)
            
    def saveNewCsvFromDataFrame(self):
        return


    def splitImageToFourDigits(self, imagePath, number):
        with Image.open(imagePath) as image:
            firstDigitRight = image.width / 4
            secondDigitRight = image.width / 2
            thirdDigitRight = image.width * 3 / 4

            firstDigit = int(number[0])
            secondDigit = int(number[1])
            thirdDigit = int(number[2])
            fourthDigit = int(number[3])

            if(self.digitsImagesCounterDataFrame[firstDigit - 1]['NumberOfInstancesFirstDigit'] <= 10000):
                firstCroppedImage = image.crop((0, 0, firstDigitRight, image.height))
                firstCroppedImage.save(f'/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/Data/{firstDigit}_{uuid.uuid4()}.png')
                self.digitsImagesCounterDataFrame.at[firstDigit - 1]['NumberOfInstancesFirstDigit'] += 1

            if(self.digitsImagesCounterDataFrame[secondDigit - 1]['NumberOfInstancesFirstDigit'] <= 10000):
                secondCroppedImage = image.crop((firstDigitRight, 0, secondDigitRight, image.height))
                secondCroppedImage.save(f'/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/Data/{secondDigit}_{uuid.uuid4()}.png')
                self.digitsImagesCounterDataFrame[secondDigit] += 1

            if(self.digitsImagesCounterDataFrame[thirdDigit - 1]['NumberOfInstancesFirstDigit'] <= 10000):
                thirdCroppedImage = image.crop((secondDigitRight, 0, thirdDigitRight, image.height))
                thirdCroppedImage.save(f'/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/Data/{thirdDigit}_{uuid.uuid4()}.png')
                self.digitsImagesCounterDataFrame[thirdDigit] += 1

            if(self.digitsImagesCounterDataFrame[fourthDigit - 1]['NumberOfInstancesFirstDigit'] <= 10000):
                fourthCroppedImage = image.crop((thirdDigitRight, 0, image.width, image.height))
                fourthCroppedImage.save(f'/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/Data/{fourthDigit}_{uuid.uuid4()}.png')
                self.digitsImagesCounterDataFrame[fourthDigit] += 1
                
    def getUpdatedDigitsImagesCounterDataFrame(self):
        try:
            with open(self.csvFileName) as file:
                content = file.readlines()
            header = content[:1]
            data = content[1:]
        except:
            header = ['digit', 'NumberOfInstancesFirstDigit', 'NumberOfInstancesSecondDigit', 'NumberOfInstancesThirdDigit', 'NumberOfInstancesFourthDigit']
            data = [[1, 0, 0, 0, 0], 
                    [2, 0, 0, 0, 0],
                    [3, 0, 0, 0, 0], 
                    [4, 0, 0, 0, 0], 
                    [5, 0, 0, 0, 0], 
                    [6, 0, 0, 0, 0], 
                    [7, 0, 0, 0, 0], 
                    [8, 0, 0, 0, 0], 
                    [9, 0, 0, 0, 0]]
            with open(self.csvFileName, 'w', newline="") as file:
                csvWriter = csv.writer(file)
                csvWriter.writerow(header)
                csvWriter.writerows(data)
        finally: 
            digitsImagesCounterdataFrame = pd.read_csv(self.csvFileName)
            return digitsImagesCounterdataFrame
            


        

        








