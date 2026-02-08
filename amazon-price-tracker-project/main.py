
from bs4 import BeautifulSoup
import requests
from smtplib import SMTP
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText


load_dotenv()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"
email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")
receiver_email = os.getenv("TO_EMAIL")
amazon_item_url = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.5",
    "Priority": "u=0, i",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
}

response = requests.get(amazon_item_url, headers=headers)
data = response.text

soup = BeautifulSoup(data, "html.parser")
price_a_whole = soup.find(name="span", class_="a-price-whole").getText()
price_a_fraction = soup.find(name="span", class_="a-price-fraction").getText()
total_price = float(f"{price_a_whole}{price_a_fraction}")

item_title = soup.find(name="span", class_="a-size-large product-title-word-break").getText()
modified_item_title = " ".join(item_title.replace("\n", "").replace("\r", "").split())


msg = MIMEText(f"{modified_item_title} is now Aed{total_price}", _charset="utf-8")
msg["Subject"] = "Instant Pot Price Alert"
msg["From"] = email
msg["To"] = receiver_email



target_price = 420

if total_price <= target_price:
    with SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.send_message(msg)
