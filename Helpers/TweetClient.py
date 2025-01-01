import os
import time
import requests
import tweepy
from Helpers import Data
from dotenv.main import load_dotenv


class TwitterBot:
    def __init__(self):
        load_dotenv()
        self.client = tweepy.Client(
            consumer_key=os.environ["CONSUMER_KEY"],
            consumer_secret=os.environ["CONSUMER_SECRET"],
            access_token=os.environ["ACCESS_TOKEN"],
            access_token_secret=os.environ["ACCESS_SECRET"],
        )
        self.auth = tweepy.OAuth1UserHandler(
            os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"]
        )
        self.auth.set_access_token(
            os.environ["ACCESS_TOKEN"], os.environ["ACCESS_SECRET"]
        )
        self.api = tweepy.API(self.auth)

    # TO BE USED IF HOSTED IN RENDER
    # def __init__(self):
    #     with open("/etc/secrets/CONSUMER_KEY", "r") as f:
    #         consumer_key = f.read().strip()
    #     with open("/etc/secrets/CONSUMER_SECRET", "r") as f:
    #         consumer_secret = f.read().strip()
    #     with open("/etc/secrets/ACCESS_TOKEN", "r") as f:
    #         access_token = f.read().strip()
    #     with open("/etc/secrets/ACCESS_SECRET", "r") as f:
    #         access_secret = f.read().strip()

    #     self.client = tweepy.Client(
    #         consumer_key=consumer_key,
    #         consumer_secret=consumer_secret,
    #         access_token=access_token,
    #         access_token_secret=access_secret,
    #     )
    #     self.auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    #     self.auth.set_access_token(access_token, access_secret)
    #     self.api = tweepy.API(self.auth)

    def tweet(self, tweet_text):
        now = time.localtime()
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", now)
        try:
            if len(tweet_text) <= 280:
                # print(f"TWEET:{tweet_text}")
                response = self.client.create_tweet(text=tweet_text)
                # print(f"Tweeted: {response}")
                msg = f"{response} at {time_str}"
                print(msg)
                return response
            else:
                # print(f"TWEET Thread:{tweet_text}")
                return self.tweet_thread(tweet_text)

        except Exception as e:
            error_msg = str(e)
            if "Status is a duplicate" in error_msg:
                print("Skipping duplicate content...")
                msg = f"Skipping duplicate content... at {time_str}"
                print(msg)
            elif "429 Too Many Requests" in error_msg:
                print("Rate limit exceeded. Waiting for 5 hours...")
                time.sleep(60 * 60 * 5)
                self.tweet(self, tweet_text)
            else:
                print(f"Error occurred while tweeting: {error_msg}")
                msg = f"{error_msg} at {time_str}"
                print(msg)
            return None

    def tweet_thread(self, tweet_text):
        now = time.localtime()
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", now)
        tweet_texts = Data.split_long_sentence(tweet_text)
        response = None
        try:
            response = self.client.create_tweet(text=tweet_texts[0])
            # print(f"Tweeted: {response}")
            main_tweet_id = response.data["id"]
            msg = f"{response} at {time_str}"
            # print(msg)
            for tweet in tweet_texts[1:]:
                response = self.client.create_tweet(
                    text=tweet, in_reply_to_tweet_id=main_tweet_id
                )
                # print(f"Tweeted: {response}")
                main_tweet_id = response.data["id"]
                msg = f"{response} at {time_str}"
                print(msg)
        except Exception as e:
            error_msg = str(e)
            if "Status is a duplicate" in error_msg:
                print("Skipping duplicate content...")
                msg = f"Skipping duplicate content... at {time_str}"
                print(msg)
            elif "429 Too Many Requests" in error_msg:
                print("Rate limit exceeded. Waiting for 5 hours...")
                time.sleep(60 * 60 * 5)
                self.tweet_thread(tweet_text)
            else:
                print(f"Error occurred while tweeting: {error_msg}")
                msg = f"{error_msg} at {time_str}"
                print(msg)
        return response

    def i_tweet(self, link):
        response = requests.get(link)
        if response.status_code == 200:
            with open("temp.jpg", "wb") as f:
                f.write(response.content)
            media = self.api.media_upload("temp.jpg")
            # print(f"media id: {media.media_id}")
            response = self.client.create_tweet(media_ids=[media.media_id])
            # print(response)
            os.remove("temp.jpg")
            return response
        else:
            print("Failed to download the image.")
            return None

    def v_tweet(self, status, video_path):
        # TODO: ADD Video tweeting
        print("not implemented")
        pass
