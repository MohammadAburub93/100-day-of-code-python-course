import time

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

PROMISED_DOWN = 250
PROMISED_UP = 150

load_dotenv()
CHROME_DRIVER_PATH = "/Users/moham/Development/chromedriver"
twitter_email = os.getenv("TWITTER_EMAIL")
twitter_password = os.getenv("TWITTER_PASSWORD")
SPEED_TEST_URL = "https://www.speedtest.net/"
TWITTER_URL = "https://x.com/"


class InternetTwitterSpeedBot:
    def __init__(self):
        self.chrome_options = ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.up_speed = 0
        self.down_speed = 0

    def get_internet_speed(self):
        self.driver.get(SPEED_TEST_URL)
        test_button = self.driver.find_element(By.CLASS_NAME, value="js-start-test")
        test_button.click()

        time.sleep(50)

        self.down_speed = self.driver.find_element(By.CLASS_NAME, value="download-speed").text
        self.up_speed = self.driver.find_element(By.CLASS_NAME, value="upload-speed").text

    def tweet_at_provider(self):

        time.sleep(5)
        self.driver.get(TWITTER_URL)
        sign_in_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[4]/a/div')))
        sign_in_button.click()
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text")))
        email_input.send_keys(twitter_email)
        next_to_password = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div')))
        next_to_password.click()
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password")))
        password_input.send_keys(twitter_password)
        next_button = self.driver.find_element(By.CLASS_NAME, value="css-1jxf684")
        next_button.click()

        twit_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "public-DraftStyleDefault-block")))
        twit_input.send_keys(f"Hey Zain, Why is my internet speed {self.down_speed}down/{self.up_speed}up"
                             f" when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?")
        post_button = self.driver.find_element(By.CLASS_NAME, value="css-175oi2r")
        post_button.click()


internet_speed_bot = InternetTwitterSpeedBot()

internet_speed_bot.get_internet_speed()

internet_speed_bot.tweet_at_provider()
