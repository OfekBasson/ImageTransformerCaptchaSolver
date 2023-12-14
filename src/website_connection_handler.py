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

NUMBER_OF_WANTED_INSTANCES_OF_EACH_NUMBER_ON_EACH_LOCATION = 250

class WebsiteConnectionHandler:
    
    def __init__(self):
        self.csvFileName = 'digits_images_counter.csv'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.digitsImagesCounterDataFrame = self.getUpdatedDigitsImagesCounterDataFrame()
        self.tabsAndNumbersDictionary = {}

    def createDatabase(self):
        while(not self.finishedFetchingAllData()):
            self.fillDataAndSubmit()
            number, imageURL = self.getURLAndStringOfNumberDisplayed()
            if (not self.finishedFetchingAllDigits(number)):
                self.createNewTab(imageURL)
                self.saveImagesOfSpecificNumber(imageURL, number)
                self.driver.close()
    
    def SaveImageForCaptchaHack(self):
        self.fillDataAndSubmit()
        self.saveImagesOfSpecificNumber(singleImage=True)
        
    
    def createNewTab(self, imageURL):
        self.driver.switch_to.new_window('tab')
        self.driver.get(imageURL)

    def finishedFetchingAllDigits(self, number):
        firstDigit = int(number[0])
        secondDigit = int(number[1])
        thirdDigit = int(number[2])
        fourthDigit = int(number[3])
        if(self.digitsImagesCounterDataFrame.at[firstDigit, 'NumberOfInstancesFirstDigit'] >= NUMBER_OF_WANTED_INSTANCES_OF_EACH_NUMBER_ON_EACH_LOCATION
           or self.digitsImagesCounterDataFrame.at[secondDigit, 'NumberOfInstancesSecondDigit'] >= NUMBER_OF_WANTED_INSTANCES_OF_EACH_NUMBER_ON_EACH_LOCATION
           or self.digitsImagesCounterDataFrame.at[thirdDigit, 'NumberOfInstancesThirdDigit'] >= NUMBER_OF_WANTED_INSTANCES_OF_EACH_NUMBER_ON_EACH_LOCATION
           or self.digitsImagesCounterDataFrame.at[fourthDigit, 'NumberOfInstancesFourthDigit'] >= NUMBER_OF_WANTED_INSTANCES_OF_EACH_NUMBER_ON_EACH_LOCATION):
            return True
        return False
        
    def enterNumberToCaptcha(self, number):
        captchaInput = self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_RadCaptcha1_CaptchaTextBox"]')
        captchaInput.send_keys(number)
        time.sleep(15)
        submitButton = self.driver.find_element(By.XPATH, '//*[@id="ContentUsersPage_btnIshur"]')
        submitButton.click()
        
    
    def finishedFetchingAllData(self):
        dataFrameHeaderValues = ['NumberOfInstancesFirstDigit', 'NumberOfInstancesSecondDigit', 'NumberOfInstancesThirdDigit', 'NumberOfInstancesFourthDigit']
        for i in range(9):
            for columnName in dataFrameHeaderValues:
                if (self.digitsImagesCounterDataFrame.at[i, columnName] < NUMBER_OF_WANTED_INSTANCES_OF_EACH_NUMBER_ON_EACH_LOCATION):
                    return False
        return True
    
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

    def saveImagesOfSpecificNumber(self, imageURL="", number='1234', singleImage=False):
        numberOfImagesToSave = 1 if singleImage else 25
        imageRegion = (806, 614, 180, 48) if not singleImage else (904, 582, 180, 48)
        for i in range(numberOfImagesToSave):
            myScreenshot = pyautogui.screenshot(region=imageRegion)
            directory = "single_image" if singleImage else "Data"
            imagePath = f'/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/{directory}/{number}.png'
            myScreenshot.save(imagePath)
            self.splitImageToFourDigits(imagePath, number, singleImage)
            os.remove(imagePath)
            time.sleep(2)
            if not singleImage:
                self.driver.get(imageURL)
        self.digitsImagesCounterDataFrame.to_csv(self.csvFileName)

    def splitImageToFourDigits(self, imagePath, number, singleImage):
        with Image.open(imagePath) as image:
            firstDigitRight, secondDigitRight, thirdDigitRight = image.width / 4, image.width / 2, image.width * 3 / 4
            firstDigit, secondDigit, thirdDigit, fourthDigit = int(number[0]), int(number[1]), int(number[2]), int(number[3])
            digitsAndLabelsData = [{'digit': firstDigit, 'label': 'NumberOfInstancesFirstDigit', 'sideBorders': {'leftBorder': 0, 'rightBorder': firstDigitRight}}, 
                      {'digit': secondDigit, 'label': 'NumberOfInstancesSecondDigit', 'sideBorders': {'leftBorder': firstDigitRight, 'rightBorder': secondDigitRight}}, 
                      {'digit': thirdDigit, 'label': 'NumberOfInstancesThirdDigit', 'sideBorders': {'leftBorder': secondDigitRight, 'rightBorder': thirdDigitRight}}, 
                      {'digit': fourthDigit, 'label': 'NumberOfInstancesFourthDigit', 'sideBorders': {'leftBorder': thirdDigitRight, 'rightBorder': image.width}}
                      ]
            for i in range(4):
                digitData = digitsAndLabelsData[i]
                self.saveDigitImage(image, digitData['digit'], digitData['label'],digitData['sideBorders'], singleImage)


    def saveDigitImage(self, image, digit, label, sideBorders, singleImage):
        if(self.digitsImagesCounterDataFrame.at[digit, label] < NUMBER_OF_WANTED_INSTANCES_OF_EACH_NUMBER_ON_EACH_LOCATION or singleImage):
                croppedImage = image.crop((sideBorders['leftBorder'], 0, sideBorders['rightBorder'], image.height))
                destinationDirectory = 'Data' if not singleImage else 'single_image'
                croppedImage.save(f'/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/{destinationDirectory}/{digit}_{uuid.uuid4()}.png')
                self.digitsImagesCounterDataFrame.at[digit, label] += 1
                
    def getUpdatedDigitsImagesCounterDataFrame(self):
        try:
            with open(self.csvFileName) as file:
                content = file.readlines()
            header = content[:1]
            data = content[1:]
        except:
            header = ['digit', 'NumberOfInstancesFirstDigit', 'NumberOfInstancesSecondDigit', 'NumberOfInstancesThirdDigit', 'NumberOfInstancesFourthDigit']
            data = [[0, 0, 0, 0, 0], 
                    [1, 0, 0, 0, 0], 
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
            


        

        








