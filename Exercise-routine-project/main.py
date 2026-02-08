
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

load_dotenv()
email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")

chrome_options = ChromeOptions()
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")


driver = webdriver.Chrome(options=chrome_options)
driver.get("https://appbrewery.github.io/gym/")



login_button = driver.find_element(By.CLASS_NAME, value="Navigation_button__uyKX2")
login_button.click()

email_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email-input")))
email_bar.send_keys(email)

password_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password-input")))
password_bar.send_keys(password)

login_submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submit-button")))
login_submit.click()





class_schedule = (WebDriverWait(driver, 10)
                  .until(EC.presence_of_element_located((By.CLASS_NAME, "Navigation_navLink__ZxeLk"))))
class_schedule.click()


days_group = driver.find_elements(By.CSS_SELECTOR, "div[id^='day-group-']")
target_days = []
for day in days_group:
    if "Tue" in day.text or "Thu" in day.text:
        target_days.append(day)


booked_counter = 0
waitlist_counter = 0
total_joined_counter = 0
already_booked_waitlisted = 0

new_booking_list = []
new_waitlist_list = []

for day in target_days:
    day_classes = day.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")
    for exc in day_classes:
        if "6:00 PM" in exc.find_element(By.CLASS_NAME, value="ClassCard_classDetail__Z8Z8f").text:
            class_button = exc.find_element(By.CSS_SELECTOR, value="div button")
            new_booking = exc.find_element(By.TAG_NAME, 'h3').text
            new_waitlist = exc.find_element(By.TAG_NAME, 'h3').text
            if class_button.text == "Book Class":
                class_button.click()
                booked_counter += 1
                print(f"✓ Booked: {new_booking} on {day.find_element(By.TAG_NAME, value='h2').text}\n")
                new_booking_list.append(f"[New Booking] {new_booking} on {day.find_element(By.TAG_NAME, value='h2').text}")
            elif class_button.text == "Booked":
                print(f"✓ Already booked: {new_booking} on {day.find_element(By.TAG_NAME, value='h2').text}\n")
                already_booked_waitlisted += 1
            elif class_button.text == "Waitlisted":
                print(f"✓ Already on waitlist: {new_booking} on {day.find_element(By.TAG_NAME, value='h2').text}\n")
                already_booked_waitlisted += 1
            elif class_button.text == "Join Waitlist":
                class_button.click()
                waitlist_counter += 1
                print(f"✓ Joined waitlist for: {new_booking} on {day.find_element(By.TAG_NAME, value='h2').text}\n")
                new_waitlist_list.append(f"[New Waitlist] {new_waitlist} on {day.find_element(By.TAG_NAME, value='h2').text}")

my_bookings = driver.find_element(By.ID, value="my-bookings-link")
my_bookings.click()
#
confirmed_joined = (WebDriverWait(driver, 10)
                    .until(EC.presence_of_all_elements_located((By.CLASS_NAME, "MyBookings_bookingCard__VRdrR"))))

total_joined_counter += len(confirmed_joined)
#
print(f"--- BOOKING SUMMARY ---\n"
      f"Classes booked: {booked_counter}\n"
      f"Waitlists joined: {waitlist_counter}\n"
      f"Already booked/waitlisted: {already_booked_waitlisted}\n"
      f"Total Tuesday & Thursday 6pm classes processed: {total_joined_counter}\n")

print("--- DETAILED CLASS LIST ---\n")
for new in new_booking_list:
    print(new)
for new in new_waitlist_list:
    print(new)






