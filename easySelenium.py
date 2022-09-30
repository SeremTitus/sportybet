#!/usr/bin/python3
import sys
import os
import  time
from selenium import webdriver

class easySelenium:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    chrome_data = os.path.join(sys.path[0], "chrome_data")
    if sys.platform ==('linux1' or'linux2'):
        driver_location ="/usr/bin/chromedriver" or os.path.join(sys.path[0], "chromedriver")
        chrome_location ="/usr/bin/google-chrome"
        options.binary_location = chrome_location
    elif sys.platform == 'win32':   
        driver_location =os.path.join(sys.path[0], "chromedriver.exe")
        options.add_argument("user-data-dir="+str(chrome_data))
    browser:any
    firstTabSet:bool = False
    isBrowserOff:bool = False
    def __init__(self,headerless:bool=False) -> None:
        self.options.headless = headerless
        self.browser = webdriver.Chrome(executable_path=self.driver_location,options=self.options)
    def isExist(self,by='By.XPATH',xpath:str =""):
        '''
        'by' parameter can satisfied with:
        [
            By.XPATH -------> DEFAULT
            By.NAME
            By.LINK_TEXT
            By.CLASS_NAME
            By.CSS_SELECTOR
            By.PARTIAL_LINK_TEXT
            By.ID            
            By.TAG_NAME            
        ]

        '''
        try:
            self.browser.find_element(by=by,value = xpath)
            return True
        except:
            return False
    def waitUntillExist(self,by='By.XPATH',xpath:str ="",timeout:int=600,inbetweenSleep:int = 0):
        clock:int=0
        while True:
            if self.isExist(by=by,xpath=xpath):
                return True
            else:
                ##Rough clock for timeout//could be done better
                time.sleep(1)
                clock += 1
                if clock >= timeout:
                    return False
                ##                
                time.sleep(inbetweenSleep)
    def switchTab(self,tab:int=0)  -> None:
       self.browser.switch_to.window(self.browser.window_handles[tab])
    def scroll(self,timeout:int=120,pageloadSleep:int=5)  -> None:
        pageHeight = self.browser.execute_script("return document.documentElement.scrollHeight")
        previousHeight = 0
        clock:int = 0
        while True:
            if previousHeight == pageHeight:
                break
            previousHeight = pageHeight
            self.browser.execute_script("window.scrollTo(0, " + str(pageHeight) + ");")
            time.sleep(pageloadSleep)
            pageHeight = self.browser.execute_script("return document.documentElement.scrollHeight")
            ##Another Rough clock for timeout//could be done better
            clock += pageloadSleep
            if clock >= timeout:
                break            ##
    def free(self) -> None:
        self.browser.quit()
        self.isBrowserOff = True
    def open(self,url:str) -> None:
        ##ensure https:// is in url
        strpos:int = 0
        for i in url:
            if i == 'https://'[strpos]:
                strpos += 1
            if strpos == 0:
                url = 'https://' + url
                break
            elif strpos >= 7:
                break
        ##
        if self.isBrowserOff:#Reopening browser once quit 
            self.__init__(self.options.headless)
            self.firstTabSet = False
            self.isBrowserOff:bool = False
        if self.firstTabSet:
            self.browser.execute_script("window.open('"+ url +"','_blank');")
            self.switchTab(len(self.browser.window_handles)-1)
        
        self.browser.get(url)
        self.firstTabSet = True
       
