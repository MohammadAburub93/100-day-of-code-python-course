import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_FORM_URL = os.getenv("GOOGLE_FORM_URL")
ZILOW_URL = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(ZILOW_URL)
properties_page = response.text

soup = BeautifulSoup(properties_page, "html.parser")

properties_links = []
properties_prices = []
properties_addresses = []

properties = soup.find_all(name="li", class_="ListItem-c11n-8-84-3-StyledListCardWrapper")

for item in properties:
    a_tag = item.find("a")
    properties_links.append(a_tag.get("href"))
    span_tag = item.find("span")
    properties_prices.append(span_tag.getText().strip("+/mo").strip("+ 1 bd"))
    address_tag = item.find("address")
    properties_addresses.append(address_tag.getText().strip().replace("|", ","))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

for num in range(len(properties) - 1):
    driver.get(GOOGLE_FORM_URL)
    address_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    WebDriverWait(driver, 20).until(lambda d: address_input.is_enabled())
    address_input.send_keys(f"{properties_addresses[num]}")
    price_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    WebDriverWait(driver, 20).until(lambda d: price_input.is_enabled())
    price_input.send_keys(f"{properties_prices[num]}")
    link_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    WebDriverWait(driver, 20).until(lambda d: link_input.is_enabled())
    link_input.send_keys(f"{properties_links[num]}")

    submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()
    time.sleep(3)






