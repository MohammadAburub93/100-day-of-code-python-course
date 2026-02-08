import time

from config import send_email

import requests
from datetime import datetime

MY_LAT = 45.559354  # Your latitude
MY_LONG = 20.554896  # Your longitude
TIME_ZONE = "Asia/Amman"


def iss_is_around():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if -5 < (iss_latitude - MY_LAT) < 5 and -5 < (iss_longitude - MY_LONG) < 5:
        return True
    else:
        return False


#Your position is within +5 or -5 degrees of the ISS position.


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "tzid": TIME_ZONE,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    the_hour_now = time_now.hour
    if sunrise > the_hour_now > sunset:
        return True
    else:
        return False


while True:
    time.sleep(60)
    if iss_is_around() and is_night():
        send_email()
