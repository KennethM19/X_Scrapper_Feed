import json
import time
import requests
from openai import OpenAI, OpenAIError
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.edge.service import Service as EdgeServ
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

service = EdgeServ(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service)
passwordInput = "//input[@name='password']"
cookies_file = "twitter_cookies.json"
verifyCode = "//li[contains(@role,'listitem')]"
homeFeed = "//div[contains(@data-testid,'primary')]//div[contains(@class,'r-aqfbo4')]//div[contains(@role,'presentation')][1]"
followFeed = "//div[contains(@data-testid,'primary')]//div[contains(@class,'r-aqfbo4')]//div[contains(@role,'presentation')][2]"
enterNumInput = "//input[@data-testid='ocfEnterTextTextInput']"
userName = ".//div[contains(@data-testid,'User-Name')]//a[@tabindex]//span"
bodyTextUser = ".//div[contains(@dir,'auto') and not(ancestor::div[@aria-labelledby])]/span"
videoLink = ".//div[contains(@data-testid,'videoComponent')]//video"
imgLink = ".//div[contains(@data-testid,'tweetPhoto')]//img"
articlesSection = "//article"
skipElementXpath = "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[5]/section/div/div/div[3]/div/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[2]"


def login():
    driver.get("https://twitter.com/login")
    time.sleep(5)

    try:
        username = driver.find_element(By.XPATH, '//input')
        buttonNext = driver.find_element(By.XPATH, '//button[2]')

        email = input("Enter your email: ")
        username.send_keys(email)
        buttonNext.click()
        time.sleep(3)

    except NoSuchElementException:
        print("An error occurred while trying to load the page, please try again")

    if element_exists(enterNumInput):
        numberInput = driver.find_element(By.XPATH, '//input[@data-testid="ocfEnterTextTextInput"]')
        nextButton = driver.find_element(By.XPATH, '//button[@data-testid="ocfEnterTextNextButton"]')
        number = input("Enter your phone number: ")
        numberInput.send_keys(number)
        nextButton.click()
        time.sleep(3)

    try:
        password = driver.find_element(By.XPATH, "//input[@name='password']")
        buttonLogin = driver.find_element(By.XPATH, "//button[contains(@data-testid,'Login')]")

        passwordText = input("Enter your password: ")
        password.send_keys(passwordText)
        buttonLogin.click()
        time.sleep(3)
    except NoSuchElementException:
        print("An error occurred while trying to load the page, please try again")

    if element_exists(verifyCode):
        codeInput = driver.find_element(By.XPATH, '//input[@data-testid="ocfEnterTextTextInput"]')
        nextButton = driver.find_element(By.XPATH, '//button[@data-testid="ocfEnterTextNextButton"]')
        code = input("Enter code: ")
        codeInput.send_keys(code)
        nextButton.click()
        time.sleep(3)

    WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.XPATH, "//header")))


def element_exists(element):
    try:
        driver.find_element(By.XPATH, element)
        return True
    except NoSuchElementException:
        return False


def select_option_feed(option):
    match option.upper():
        case 'FOR YOU' | '1':
            feed = driver.find_element(By.XPATH, homeFeed)
            feed.click()

        case 'FOLLOWING' | '2':
            feed = driver.find_element(By.XPATH, followFeed)
            feed.click()

    time.sleep(5)


def generate_tweets(number_tweets):
    tweets = []
    while len(tweets) < number_tweets:
        articles = driver.find_elements(By.XPATH, articlesSection)

        for article in articles:
            if len(tweets) >= number_tweets:
                break

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
                tweet['video'] = video_element.get_attribute('poster')
            except NoSuchElementException:
                tweet['video'] = None

            tweets.append(tweet)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    return tweets


login()

option_feed = input("Enter the feed option (1-Four you / 2-Following): ")
number_tweets = int(input("Enter the number of tweets to scrape: "))

select_option_feed(option_feed)

tweets = generate_tweets(number_tweets)

# Exportar la lista de tweets a un archivo JSON con codificación UTF-8
with open('tweets_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(tweets, json_file, indent=4, ensure_ascii=False)

print("Data saved to tweets_data.json")
