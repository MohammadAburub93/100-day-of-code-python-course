
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


driver = webdriver.Chrome(options=chrome_options)
driver.get("https://ozh.github.io/cookieclicker/")


select_lang = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "langSelect-EN")))
select_lang.click()


cookie_button = driver.find_element(By.ID, value="bigCookie")
try:
    cookie_button.click()
except:
    cookie_button = driver.find_element(By.ID, value="bigCookie")


time_out = time.time() + 60*5
time_check = time.time() + 5
enabled_list = []


while time.time() < time_out:
    if time.time() >= time_check:
        upgrade_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "unlocked")))
        for fun in upgrade_buttons:
            separated = fun.get_attribute(name="class").split()
            if "enabled" in separated:
                enabled_list.append(fun)
        if len(enabled_list) != 0:
            reversed_upgrade_buttons = enabled_list[::-1]
            reversed_upgrade_buttons[0].click()
        time_check += 5

    cookie_button.click()


per_second = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cookiesPerSecond")))

per_second_value = per_second.text.strip("per second:")

print(f"cookies/second: {per_second_value}")

driver.quit()





