from dotenv import load_dotenv
from random import randint
import os, d
import pandas
import datetime as dt
import smtplib

load_dotenv()
email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")


birthdays_data = pandas.read_csv("birthdays.csv")
birthdays_data.at[1, "name"] = "mum"
birthdays_data.at[1, "email"] = "mohammad.aburub.t.93@gmail.com"
birthdays_data.at[1, "year"] = 1993
birthdays_data.at[1, "month"] = 11
birthdays_data.at[1, "day"] = 27


birthdays_dict = birthdays_data.to_dict(orient="records")
today_date = dt.datetime.now()
month_now = today_date.month
day_now = today_date.day
random_letter_number = randint(1, 3)
for person in birthdays_dict:
    if person["month"] == month_now and person["day"] == day_now:
        with open(f"./letter_templates/letter_{random_letter_number}.txt") as random_letter:
            letter = random_letter.read()

        modified_letter = letter.replace("[NAME]", person["name"])
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email,
                             password=password)
            connection.sendmail(from_addr=email,
                                to_addrs=person["email"],
                                msg=f"Subject:Happy Birthday\n\n{modified_letter}")
    else:
        pass













