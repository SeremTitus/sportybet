import time

from selenium.webdriver.common.by import By

from easySelenium import easySelenium


class sp(easySelenium):
    def __init__(self,headerless =False, username ='0746336315', password ='acc1youtube'):
        self.username = username
        self.password = password
        super().__init__(headerless)
        self.login()
    def login(self):
        self.open('https://www.sportybet.com/ke/sport/football/live_list')
        self.waitUntillExist('/html/body')
        if self.isExist('//*[@id="j_page_header"]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[1]/button') and self.browser.find_element(By.XPATH,'//*[@id="j_page_header"]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[1]/button').is_displayed():
            self.browser.find_element(By.XPATH,'//*[@id="j_page_header"]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]/input').clear()
            self.browser.find_element(By.XPATH,'//*[@id="j_page_header"]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]/input').send_keys(self.username)
            self.browser.find_element(By.XPATH,'//*[@id="j_page_header"]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[1]/input').send_keys(self.password)
            self.browser.find_element(By.XPATH,'//*[@id="j_page_header"]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[1]/button').click()
        self.sportSelection()
    def sportSelection(self):
        self.waitUntillExist('/html/body')
        if self.isExist('/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div'):
            self.browser.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div').click()
    def findMatch(self,match='CSC Dumbravita:CFR Cluj'):
        '''
        match = str([homeTeamName]),':',str([homeTeamName])
        example = "CSC Dumbravita:CFR Cluj"
        '''
        #/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[3]/div[2]/div[1]/div[2]
        #/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]
        #/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[2]
        #/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]
        #/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]
        #/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[1]
        #/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[2]
        cardinality =1
        mcat_xpath = '/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div['+str(cardinality)+']'
        while True:
            mcat_xpath = '/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div['+str(cardinality)+']'
            if self.isExist(str(mcat_xpath)):
                sub_cardinality = 2
                while True:
                    m_xpath =  mcat_xpath+'/div[1]/div['+str(sub_cardinality)+']'
                    if self.isExist(str(m_xpath)):
                        homem_xpath =str(m_xpath)+'/div[1]/div[2]/div[2]/div[1]'
                        awaym_xpath =m_xpath+'/div[1]/div[2]/div[2]/div[2]'
                        print(homem_xpath)
                        homem_name =self.browser.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]')
                        homem_name = homem_name.text
                        print(homem_name)
                        awaym_name =self.browser.find_element(By.XPATH,awaym_xpath).text
                        print((str(homem_name+':'+awaym_name)))
                        print(match)
                        if (str(homem_name+':'+awaym_name)) == match:
                            print(m_xpath)
                            #return m_xpath
                    else:
                        break
                    sub_cardinality += 1
            else:
                break
            cardinality = cardinality +1
        

h = sp()
h.findMatch()
print('not found')
time.sleep(30)