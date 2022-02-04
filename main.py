import requests
from datetime import datetime
# import smtplib
import time

MY_LAT = 50.075539  # Your latitude
MY_LONG = 14.437800  # Your longitude


# Your position is within +5 or -5 degrees of the ISS position.
def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if abs(iss_latitude - MY_LAT) < 5 and abs(iss_longitude - MY_LONG) < 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response_sunset = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response_sunset.raise_for_status()
    data_sunset = response_sunset.json()
    sunrise = int(data_sunset["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data_sunset["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True


def send_mail():
    sender = "Michal <michal@michal.com>"
    receiver = "Me <mikhael@centrum.cz>"

    message = f"""\
                Subject: ISS Overhead!
                To: {receiver}
                From: {sender}

                \nHello! ISS is now above your head!"""

    print(message)
    print("------------------------")

    # with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
    #     server.starttls()
    #     server.login("e459c3f6880fcc", "26c63def9cd9c8")
    #     server.sendmail(sender, receiver, message)


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
while True:
    if iss_overhead() and is_night():
        send_mail()
    time.sleep(60)
