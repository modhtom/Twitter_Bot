import requests
import datetime

def get_islamic_date():
    try:
        response = requests.get("https://api.aladhan.com/v1/gToH/" + datetime.datetime.now().strftime("%d-%m-%Y"))
        data = response.json()

        day = data['data']['hijri']['day']
        month = data['data']['hijri']['month']['en']

        islamic_date = f"{day} {month}"
        return islamic_date

    except requests.RequestException as e:
        print(f"Error fetching Islamic date: {e}")
        return None