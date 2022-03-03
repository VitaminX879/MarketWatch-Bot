#pip install selenium and webdriver-manager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager
import time

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

URL = 'https://marketwatch.com/'
loginURL = 'https://accounts.marketwatch.com/login?target=https%3A%2F%2Fwww.marketwatch.com%2F'

class MarketWatch:
    def __init__(self, email, password, game): #game name should be passed in the format you would find in a link (i.e. miles-private-game)

        driver.get(loginURL)

        time.sleep(1.5)
        driver.find_element(By.ID, 'username').send_keys(email)

        driver.find_element(By.CLASS_NAME, 'continue-submit').click()

        time.sleep(1.5)
        driver.find_element(By.ID, 'password-login-password').send_keys(password)

        driver.find_elements(By.CLASS_NAME, 'basic-login-submit')[1].click()

        time.sleep(1.5)
        self.game = 'games/' + game + '/portfolio'
        gameURL = URL + self.game
        driver.get(gameURL)

class Actions:
    def __init__(self, ticker, shares, orderType, term, type, price, game):

        driver.find_element(By.CLASS_NAME, 'j-miniTrade').send_keys(ticker + Keys.ENTER)

        time.sleep(1.5)
        driver.execute_script("window.scrollTo(0, 500)")

        ad = True
        while ad:
            try:
                time.sleep(1.5)
                driver.find_element(By.CLASS_NAME, 'j-trade').click()
                ad = False
            except:
                driver.find_element(By.CLASS_NAME, 'close-btn').click()


        time.sleep(1)
        driver.find_element(By.ID, 'shares').send_keys(Keys.BACKSPACE + shares)

        if orderType == 'BUY':
            driver.find_element(By.XPATH, '//label[@for="order-buy"]').click()

        elif orderType == 'SHORT':
            driver.find_element(By.XPATH, '//label[@for="order-short"]').click()

        elif orderType == 'SELL':
            driver.find_element(By.XPATH, '//label[@for="order-sell"]').click()

        elif orderType == 'COVER':
            driver.find_element(By.XPATH, '//label[@for="order-cover"]').click()

        if term == 'DAY':
            driver.find_element(By.XPATH, '//label[@for="term-day"]').click()

        elif term == 'INDEFINITE':
            driver.find_element(By.XPATH, '//label[@for="term-cancelled"]').click()

        if type == 'MARKET':
            Select(driver.find_element(By.ID, 'priceType')).select_by_value('None')

        elif type == 'LIMIT':
            Select(driver.find_element(By.ID, 'priceType')).select_by_value('Limit')
            driver.find_element(By.ID, 'stop-limit').send_keys(price)

        elif type == 'STOP':
            Select(driver.find_element(By.ID, 'priceType')).select_by_value('Stop')
            driver.find_element(By.ID, 'stop-limit').send_keys(price)

        time.sleep(1)
        driver.find_element(By.CLASS_NAME, 'j-submit').click()

        time.sleep(1.5)
        self.game = 'games/' + game + '/portfolio'
        gameURL = URL + self.game
        driver.get(gameURL)

