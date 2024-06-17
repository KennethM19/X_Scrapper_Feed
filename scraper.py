import json
import os.path
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.edge.service import Service as EdgeServ
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

service = EdgeServ(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service)
cookies_file = "twitter_cookies.json"
homeFeed = "//div[contains(@data-testid,'primary')]//div[contains(@class,'r-aqfbo4')]//div[contains(@role,'presentation')][1]"
followFeed = "//div[contains(@data-testid,'primary')]//div[contains(@class,'r-aqfbo4')]//div[contains(@role,'presentation')][2]"
enterNumInput = "//input[@data-testid='ocfEnterTextTextInput']"
userName = "//article//div[contains(@data-testid,'User-Name')]//a[@tabindex]//span"
videoLink = "//article//div[contains(@data-testid,'videoComponent')]//video"


def login_save_cookies():
    driver.get("https://twitter.com/login")
    time.sleep(5)

    username = driver.find_element(By.XPATH, '//input')
    buttonNext = driver.find_element(By.XPATH, '//button[2]')

    email = input("Enter your email: ")
    username.send_keys(email)
    buttonNext.click()
    time.sleep(5)

    if element_exists(enterNumInput):
        numberInput = driver.find_element(By.XPATH, '//input[@data-testid="ocfEnterTextTextInput"]')
        nextButton = driver.find_element(By.XPATH, '//button[@data-testid="ocfEnterTextNextButton"]')
        number = input("Enter your phone number: ")
        numberInput.send_keys(number)
        nextButton.click()
        time.sleep(5)

    password = driver.find_element(By.XPATH, "//input[@name='password']")
    buttonLogin = driver.find_element(By.XPATH, "//button[contains(@data-testid,'Login')]")

    passwordText = input("Enter your password: ")
    password.send_keys(passwordText)
    buttonLogin.click()
    time.sleep(5)

    WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.XPATH, "//header")))

    cookies = driver.get_cookies()
    with open(cookies_file, 'w') as f:
        json.dump(cookies, f)


def load_cookies_login():
    driver.get("https://twitter.com/home")
    time.sleep(5)

    if os.path.exists(cookies_file):
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)

        driver.refresh()


def element_exists(element):
    try:
        driver.find_element(By.XPATH, element)
        return True
    except NoSuchElementException:
        return False


option_feed = input("Enter the feed option (1-Four you / 2-Following): ")
number_tweets = input("Enter the number of tweets to scrape: ")

login_save_cookies()

match option_feed.upper():
    case 'FOUR YOU' | '1':
        feed = driver.find_element(By.XPATH, homeFeed)
        feed.click()

    case 'FOLLOWING' | '2':
        feed = driver.find_element(By.XPATH, followFeed)
        feed.click()

time.sleep(5)

userNames = driver.find_elements(By.XPATH, userName)
userNames_text = []

for username in userNames:
    name = username.text
    userNames_text.append(name)

for username in userNames_text:
    print(username)

driver.save_screenshot("screenshot.png")
