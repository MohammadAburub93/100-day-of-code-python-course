import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
sender_email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")
receiver_email = os.getenv("TO_EMAIL")

def send_email():
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=email,
                     password=password)
    connection.sendmail(from_addr=sender_email,
                        to_addrs=receiver_email,
                        msg="Subject:ISS nearby\n\nJust look up the iss is around you.")
