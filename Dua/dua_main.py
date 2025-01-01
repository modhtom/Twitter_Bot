from Helpers import TweetClient as client, Email as email
import requests
import traceback
import re

API_URL = "https://raw.githubusercontent.com/nawafalqari/azkar-api/56df51279ab6eb86dc2f6202c7de26c8948331c1/azkar.json"
index = 0


def fetch_api_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {API_URL}")
        return None


def tweet_azkar():
    global index
    api_data = fetch_api_data()
    if not api_data:
        return

    filtered_data = {
        "أدعية قرآنية": api_data.get("أدعية قرآنية", []),
        "أدعية الأنبياء": api_data.get("أدعية الأنبياء", []),
        "تسابيح": api_data.get("تسابيح", []),
    }

    twitter_bot = client.TwitterBot()
    try:
        flat_data = [
            item["content"]
            for category in filtered_data.values()
            for sublist in category
            for item in (sublist if isinstance(sublist, list) else [sublist])
        ]

        if index < len(flat_data):
            text = flat_data[index]
            content = re.sub(r"\\n", " ", text).strip()
            content = re.sub(r"\'", " ", text).strip()
            content = re.sub(r",", " ", text).strip()
            hashtag = "📿 #دعاء"
            tweet_content = f"🤲 {content} {hashtag}"
            if len(tweet_content) <= 270:
                twitter_bot.tweet(f"{tweet_content} 💭 شاركونا بدعائكم 🙏")
            else:
                twitter_bot.tweet_thread(
                    f" 📌 هذه سلسلة أدعية، تابعوا معنا. {tweet_content}"
                )
            index = (index + 1) % len(flat_data)
        else:
            print("All azkar have been tweeted.")
    except Exception as e:
        error_message = (
            f"An error occurred while tweeting azkar.\n"
            f"Index: {index}\n"
            f"Error Type: {type(e).__name__}\n"
            f"Error Message: {str(e)}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        print(error_message)
        email.send(error_message)
