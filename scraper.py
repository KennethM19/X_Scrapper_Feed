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
bodyTextUser = "//div[contains(@dir,'auto') and not(ancestor::div[@aria-labelledby])]/span"
videoLink = "//div[contains(@data-testid,'videoComponent')]//video"
imgLink = "//div[contains(@data-testid,'tweetPhoto')]//img"
articlesSection = "//article"


def login_save_cookies():
    driver.get("https://twitter.com/login")
    time.sleep(5)

    username = driver.find_element(By.XPATH, '//input')
    buttonNext = driver.find_element(By.XPATH, '//button[2]')

    email = input("Enter your email: ")
    username.send_keys(email)
    buttonNext.click()
    time.sleep(3)

    if element_exists(enterNumInput):
        numberInput = driver.find_element(By.XPATH, '//input[@data-testid="ocfEnterTextTextInput"]')
        nextButton = driver.find_element(By.XPATH, '//button[@data-testid="ocfEnterTextNextButton"]')
        number = input("Enter your phone number: ")
        numberInput.send_keys(number)
        nextButton.click()
        time.sleep(3)

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


def select_option_feed(option):
    match option.upper():
        case 'FOUR YOU' | '1':
            feed = driver.find_element(By.XPATH, homeFeed)
            feed.click()

        case 'FOLLOWING' | '2':
            feed = driver.find_element(By.XPATH, followFeed)
            feed.click()

    time.sleep(5)


def generate_list(xpath):
    group = []
    elements = driver.find_elements(By.XPATH, xpath)
    for element in elements:
        if xpath == 'userName' or xpath == 'bodyTextUser':
            group.append(element.text)
        elif 'imgLink' in xpath:
            group.append(element.get_attribute('src'))
        elif 'videoLink' in xpath:
            group.append(element.get_attribute('poster'))
        else:
            group.append(None)

    return group

login_save_cookies()

option_feed = input("Enter the feed option (1-Four you / 2-Following): ")
number_tweets = input("Enter the number of tweets to scrape: ")

select_option_feed(option_feed)

names = generate_list(userName)
body = generate_list(bodyTextUser)

print(names)
print(body)
