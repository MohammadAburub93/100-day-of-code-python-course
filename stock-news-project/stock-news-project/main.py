import requests
import smtplib

import os
from dotenv import load_dotenv
from data import data

load_dotenv()
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
stock_api_key = os.getenv("STOCK_API_KEY")
stock_api_key_2 = os.getenv("STOCK_API_KEY_2")
new_api_key = os.getenv("NEWS_API_KEY")
stocks_api = "https://www.alphavantage.co/query"
news_api = "https://newsapi.org/v2/everything"

email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")
receiver_email = os.getenv("TO_EMAIL")

stock_api_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api_key_2,
}

news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": new_api_key,
}


def stock_status():
    stock_response = requests.get(stocks_api, params=stock_api_parameters)
    stock_response.raise_for_status()
    # tesla_stock_data = stock_response.json()
    tesla_stock_data = data

    closing_price_list = [float(value["4. close"])for (key, value) in tesla_stock_data["Time Series (Daily)"].items()]
    closing_price_list = closing_price_list[0:2]
    yesterday_price = closing_price_list[0]
    the_day_before_price = closing_price_list[1]
    if yesterday_price > the_day_before_price:
        price_difference_percentage = round((((yesterday_price - the_day_before_price) / the_day_before_price)
                                             * 100), 2)

        stock_value = f"TSLA: raise {price_difference_percentage}%"
    else:
        price_difference_percentage = round((((the_day_before_price - yesterday_price) / the_day_before_price)
                                             * 100), 2)
        stock_value = f"TSLA: loose {price_difference_percentage}%"

    return stock_value, price_difference_percentage


def get_news():
    news_response = requests.get(news_api, params=news_parameters)
    news_response.raise_for_status()
    tesla_news = news_response.json()["articles"]
    news_list = []
    news_count = 0
    for news in tesla_news:
        if news_count < 3:
            news_dict = {"title": news["title"], "description": news["description"]}
            news_list.append(news_dict)
            news_count += 1
        else:
            pass
    return news_list


def tesla_stocks_alert():
    stock_value = stock_status()
    if stock_value[1] > 1:
        tesla_news = get_news()
        msg_to_send = (f"Subject:Stocks change alert\n\n"
                        f"{stock_value[0]}\n"
                        f"Heading:{tesla_news[0]['title']}\n"
                        f"Brief: {tesla_news[0]['description']}\n\n"
                        f"Heading:{tesla_news[1]['title']}\n"
                        f"Brief: {tesla_news[1]['description']}\n\n"
                        f"Heading:{tesla_news[2]['title']}\n"
                        f"Brief: {tesla_news[2]['description']}")

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email,
                                to_addrs=receiver_email,
                                msg=msg_to_send
                                )


tesla_stocks_alert()