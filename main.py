import datetime
import json
import time
import tweepy
from discord_webhook import DiscordWebhook

with open("secret.json") as f:
    env = json.load(f)

url = env["webhook"]
consumer_key = env["consumer_key"]
consumer_secret = env["consumer_secret"]
access_token = env["access_token"]
access_token_secret = env["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

users = env["users"]

meta = {}
for user in users:
    meta[user] = {
        "tweets": 0,
        "favorites": 0
    }
while True:
    dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    t = dt.strftime('%Y/%m/%d %H:%M:%S')
    for target in users:
        user = api.get_user(target)
        if meta[target]["tweets"] != user.statuses_count:
            content = f'  {target} tweet {meta[target]["tweets"]} -> {user.statuses_count} ({t})'
            DiscordWebhook(url=url, content=content).execute()
        meta[target]["tweets"] = user.statuses_count
        if meta[target]["favorites"] != user.favourites_count:
            content = f'  {target} favorite {meta[target]["favorites"]} -> {user.favourites_count} ({t})'
            DiscordWebhook(url=url, content=content).execute()
        meta[target]["favorites"] = user.favourites_count
    time.sleep(60)
