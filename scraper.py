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
userName = ".//div[contains(@data-testid,'User-Name')]//a[@tabindex]//span"
bodyTextUser = ".//div[contains(@dir,'auto') and not(ancestor::div[@aria-labelledby])]/span"
videoLink = ".//div[contains(@data-testid,'videoComponent')]//video"
imgLink = ".//div[contains(@data-testid,'tweetPhoto')]//img"
externalLink = ".//div[contains(@data-testid,'card.wrapper')]//a"
articlesSection = "//article"
skipElementXpath = ".//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[5]/section/div/div/div[3]/div/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[2]"


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


def generate_tweets():
    articles = driver.find_elements(By.XPATH, articlesSection)
    tweets = []

    for article in articles:
        try:
            if article.find_element(By.XPATH, skipElementXpath):
                continue
        except NoSuchElementException:
            tweet = {}
            try:
                name_element = article.find_element(By.XPATH, userName)
                tweet['name'] = name_element.text
            except NoSuchElementException:
                tweet['name'] = None

            try:
                text_element = article.find_element(By.XPATH, bodyTextUser)
                tweet['text'] = text_element.text
            except NoSuchElementException:
                tweet['text'] = None

            try:
                img_element = article.find_element(By.XPATH, imgLink)
                tweet['img'] = img_element.get_attribute('src')
            except NoSuchElementException:
                tweet['img'] = None

            try:
                video_element = article.find_element(By.XPATH, videoLink)
                tweet['video'] = video_element.get_attribute('src')
            except NoSuchElementException:
                tweet['video'] = None

            tweets.append(tweet)

    return tweets

login_save_cookies()

option_feed = input("Enter the feed option (1-Four you / 2-Following): ")
number_tweets = input("Enter the number of tweets to scrape: ")

select_option_feed(option_feed)

tweets = generate_tweets()

# Exportar la lista de tweets a un archivo JSON
with open('tweets_data.json', 'w') as json_file:
    json.dump(tweets, json_file, indent=4)

print("Data saved to tweets_data.json")

