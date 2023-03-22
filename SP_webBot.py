import time

from selenium.webdriver.common.by import By

from easySelenium import easySelenium


class sp(easySelenium):
    def __init__(self,headerless =False, username ='', password =''):
        self.username = username
        self.password = password
        super().__init__(headerless)
    def login(self):
        if self.firstTabSet and not(self.isBrowserOff):
            self.browser.get('https://www.sportybet.com/ke/sport/football/live_list')
        else:
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
        if self.isExist('//*[@id="header"]/a[1]/span[1]'):
            self.browser.find_element(By.XPATH,'//*[@id="header"]/a[1]/span[1]').click()
        if self.isExist('/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div'):
            self.browser.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div').click()
    def findMatch(self,match='') -> {}:  # type: ignore
        '''
        return  {'m_xpath':m_xpath,'winning':winning,'diff':diff}
        match = str([homeTeamName]),':',str([homeTeamName])
        example = "CSC Dumbravita:CFR Cluj"
        '''
        cardinality =1
        while True:
            mcat_xpath = '/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div['+str(cardinality)+']'
            if self.isExist(str(mcat_xpath)):
                sub_cardinality = 2
                while True:
                    m_xpath =  mcat_xpath+'/div['+str(sub_cardinality)+']'
                    if self.isExist(str(m_xpath)):
                        homem_name =self.browser.find_element(By.XPATH,(m_xpath + '/div[1]/div[2]/div[2]/div[1]')).text
                        awaym_name =self.browser.find_element(By.XPATH,(m_xpath + '/div[1]/div[2]/div[2]/div[2]')).text
                        if (str(homem_name+':'+awaym_name)) == match:
                            if int(self.browser.find_element(By.XPATH,(m_xpath + '/div[1]/div[2]/div[3]/div[1]')).text) < int(self.browser.find_element(By.XPATH,(m_xpath + '/div[1]/div[2]/div[3]/div[2]')).text):
                                winning = 'away'
                                diff = int(self.browser.find_element(By.XPATH,(m_xpath + '/div[1]/div[2]/div[3]/div[2]')).text) - int(self.browser.find_element(By.XPATH,(m_xpath + '/div[1]/div[2]/div[3]/div[1]')).text)
                            elif int(self.browser.find_element(By.XPATH,(m_xpath + '/div[1]/div[2]/div[3]/div[1]')).text) > int(self.browser.find_element(By.XPATH,(m_xpath + '/div[1]/div[2]/div[3]/div[2]')).text):
                                winning = 'home'
                                diff = int(self.browser.find_element(By.XPATH,(m_xpath + '/div[1]/div[2]/div[3]/div[1]')).text) - int(self.browser.find_element(By.XPATH,(m_xpath + '/div[1]/div[2]/div[3]/div[2]')).text)
                            else:
                                winning = 'draw'
                                diff = 0
                            return {'m_xpath':str(m_xpath),'winning':str(winning),'diff':int(diff)}
                    else:
                        break
                    sub_cardinality += 1
            else:
                return {'m_xpath':'','winning':'','diff':0}
            cardinality = cardinality +1
    def selectmatch(self,m_xpath='',market_desc ='',option=''):
        """
        market:
                 '1X2'
                 'Over/Under0.5'
        """
        self.timeoutLogins_WinningWrapper()        
        if market_desc.lower() == '1X2'.lower() and self.isExist(m_xpath):
            cardinality = 0
            match option:
                case'home':
                    cardinality = 1
                case'draw':
                    cardinality = 2
                case'away':
                    cardinality = 3
            betselected = m_xpath  + '/div[2]/div[1]/div['+ str(cardinality) +']'
            if self.browser.find_element(By.XPATH,betselected).is_enabled:
                self.browser.find_element(By.XPATH,betselected).click()
                self.sportSelection()
                return True
        elif self.isExist(m_xpath):
            self.browser.find_element(By.XPATH,(m_xpath + '/div[3]')).click()
            self.waitForUrlChange("https://www.sportybet.com/ke/sport/football/live_list")
            self.timeoutLogins_WinningWrapper()
            if self.isExist('/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/section/div/div[@class="m-detail-error"]/div/button'):
                self.browser.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/section/div/div[@class="m-detail-error"]/div/button').click()
            if self.isExist('/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/section/div/div[@class="m-detail-error"]/div/button'):
                self.login()
                return True
            self.waitUntillExist('/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/section/div[1]/div[3]/i')
            self.browser.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/section/div[1]/div[3]/i').click()
            cardinality = 1
            while True:
                market_xpath = '/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/section/div[2]/div['+str(cardinality)+']'
                if self.isExist(market_xpath):
                    desc_found = self.browser.find_element(By.XPATH,str(market_xpath+'/div[1]/div/div[1]/span[1]')).text
                    if desc_found =='Correct Score':
                        self.browser.find_element(By.XPATH,(market_xpath+'/div[1]/div/div[1]/i')).click()
                    for char in desc_found:
                        if char == '&':
                            #'Double Chance & Over/Under'
                            continue
                    if desc_found.lower() == market_desc.lower():
                        subcardinality = 1
                        while True:
                            betselected = market_xpath +'/div[2]/div/div['+str(subcardinality)+']'
                            if self.isExist(betselected):
                                if self.browser.find_element(By.XPATH,betselected).is_enabled:
                                    option_found =self.browser.find_element(By.XPATH,str(betselected+'/span[1]')).text
                                    if option_found.lower() == option.lower():
                                        self.browser.find_element(By.XPATH,betselected).click()
                                        self.sportSelection()
                                        return True                                 
                            else:
                                break
                            subcardinality += 1
                else:
                    self.sportSelection()
                    return False
                cardinality += 1    
    def clearBetslip(self):
        while self.isExist('//*[@id="j_betslip"]/div[2]/div[3]/div[1]/div[2]/div[1]') or self.isExist('//*[@id="j_betslip"]/div[2]/div[2]/div/div[2]/div[1]'):
            if self.isExist('//*[@id="j_betslip"]/div[2]/div[3]/div[1]/div[2]/div[1]'):   
                self.browser.find_element(By.XPATH,'//*[@id="j_betslip"]/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/i[2]').click()
            elif self.isExist('//*[@id="j_betslip"]/div[2]/div[2]/div/div[2]/div[1]'):
                self.browser.find_element(By.XPATH,'//*[@id="j_betslip"]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[1]/i[2]').click()
    def timeoutLogins_WinningWrapper(self):        
        if self.isExist('//*[@class="es-dialog-wrap"]/div[2]/div/div/div[@class="m-winning-wrapper"]'):
           self.browser.find_element(By.XPATH,'//*[@class="es-dialog-wrap"]/div[2]/div/div/div[@class="m-winning-wrapper"]/div/i').click()
        if self.isExist('//*[@class="m-page m-page--login"]'):
            self.browser.find_element(By.XPATH,'//*[@class="m-page m-page--login"]/section/div[2]/div/div/span/input').clear()
            self.browser.find_element(By.XPATH,'//*[@class="m-page m-page--login"]/section/div[2]/div/div/span/input').send_keys(self.username)
            self.browser.find_element(By.XPATH,'//*[@class="m-page m-page--login"]/section/div[2]/div/div[2]/span/input').clear()
            self.browser.find_element(By.XPATH,'//*[@class="m-page m-page--login"]/section/div[2]/div/div[2]/span/input').send_keys(self.username)
            if self.browser.find_element(By.XPATH,'//*[@class="m-page m-page--login"]/section/div[2]/div/div[3]/button').is_enabled:
                self.browser.find_element(By.XPATH,'//*[@class="m-page m-page--login"]/section/div[2]/div/div[3]/button').click()
            else:
                self.free()
                self.login()
    def bet(self,stake,debugmode=False):
        if self.isExist('//*[@id="j_stake_0"]/span[@class="m-input-com"]/input') and self.browser.find_element(By.XPATH,'//*[@id="j_stake_0"]/span[@class="m-input-com"]/input').is_enabled:
            self.browser.find_element(By.XPATH,'//*[@id="j_stake_0"]/span[@class="m-input-com"]/input').clear()
            self.browser.find_element(By.XPATH,'//*[@id="j_stake_0"]/span[@class="m-input-com"]/input').send_keys(stake)
        while not(self.isExist('//*[@class="es-dialog-wrap"]/div[2]/div/div/div[@class="m-dialog-wrapper m-dialog-suc"]')):
            if self.isExist('//*[@id="esDialog0"]/div[2]/div[1]/a[@class="es-dialog-close m-dialog-close"]') and self.browser.find_element(By.XPATH,'//*[@id="esDialog0"]/div[2]/div[1]/a[@class="es-dialog-close m-dialog-close"]').is_displayed:
                self.browser.find_element(By.XPATH,'//*[@id="esDialog0"]/div[2]/div[1]/a[@class="es-dialog-close m-dialog-close"]').click()
                return False
            if self.isExist('//*[@class="m-btn-wrapper"]/button[@class="af-button af-button--primary"]') and self.browser.find_element(By.XPATH,'//*[@class="m-btn-wrapper"]/button[@class="af-button af-button--primary"]').is_displayed:
                self.browser.find_element(By.XPATH,'//*[@class="m-btn-wrapper"]/button[@class="af-button af-button--primary"]').click()
            if self.isExist('//*[@class="m-comfirm-wrapper"]/div[1]/div[2]/button[@class="af-button af-button--primary"]') and self.browser.find_element(By.XPATH,'//*[@class="m-comfirm-wrapper"]/div[1]/div[2]/button[@class="af-button af-button--primary"]').is_displayed:
                if not(debugmode):
                    self.browser.find_element(By.XPATH,'//*[@class="m-comfirm-wrapper"]/div[1]/div[2]/button[@class="af-button af-button--primary"]').click()
            if self.isExist('//*[@class="m-btn-wrapper"]/button[@class="af-button af-button--primary"]') and not(self.browser.find_element(By.XPATH,'//*[@class="m-btn-wrapper"]/button[@class="af-button af-button--primary"]').is_enabled):
               return False
        if self.isExist('//*[@class="es-dialog-wrap"]/div[2]/div/div/div[@class="m-dialog-wrapper m-dialog-suc"]/div[2]/div[1]/button'):
            self.browser.find_element(By.XPATH,'//*[@class="es-dialog-wrap"]/div[2]/div/div/div[@class="m-dialog-wrapper m-dialog-suc"]/div[2]/div[1]/button').click()
            return True
    def returnBal(self):
        self.timeoutLogins_WinningWrapper()
        if self.isExist('//*[@id="j_balance"]') and not(self.isBrowserOff):
            return int(self.browser.find_element(By.XPATH,'//*[@id="j_balance"]').text)
    def placeBet(self,matchs=[{'match':'Wales:Finland','market_desc':'1X2','option':'home','winning':'home','diff':'0'}],stake=8,shoudTurnOff=False,debugmode=False):
        """
        matchs = ['str([homeTeamName]),':',str([homeTeamName])',...,...]
        example = ["CSC Dumbravita:CFR Cluj"]
        market=[
                 '1X2',
                 'Over/Under0.5'
                ]
        option:['draw',
                'home',
                'away'
            ]
        """
        if not(self.waitForInternet()):
            return False
        if self.isBrowserOff:
            self.login()
        self.clearBetslip()
        anyMatchSelected_betplaced = False
        for match in matchs:
            self.timeoutLogins_WinningWrapper()
            stats = self.findMatch(match['match'])
            if match['winning'] == stats['winning']:        
                if self.selectmatch(str(stats['m_xpath']),match['market_desc'],match['option']):
                    anyMatchSelected_betplaced = True
        if anyMatchSelected_betplaced: 
            anyMatchSelected_betplaced = self.bet(stake,debugmode)
        if shoudTurnOff and not(debugmode):
            self.free()
        return anyMatchSelected_betplaced
                            
h = sp()
print(h.placeBet(shoudTurnOff=True,debugmode=True))
time.sleep(30)