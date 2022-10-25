#!/usr/bin/env python
import json
import tweepy
from google.cloud import pubsub_v1
from google.oauth2 import service_account

# GCP

key_path = "pubsub_creds.json"
credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Pub/Sub
pubsub_client = pubsub_v1.PublisherClient(credentials=credentials)

# Pub/Sub Topic(ID, Topic)
topic_path = pubsub_client.topic_path(
    '<YOUR_PUBSUB_ID>', '<YOUR_PUBSUB_TOPIC>')

# # Twitter API Key / Access Token
twitter_api_key = 'YOUR_API_KEY'
twitter_api_secret_key = 'YOUR_API_SECRET_KEY'
twitter_access_token = 'YOUR_ACCESS_TOKEN'
twitter_access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'


class TweetStreamer(tweepy.Stream):

    def on_status(self, status):
        tweet = json.dumps(
            {'id': status.id, 'created_at': status.created_at, 'text': status.text}, default=str)
        print(tweet)
        pubsub_client.publish(topic_path, data=tweet.encode('utf-8'))

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False


# Initialize instance of the subclass
streamer = TweetStreamer(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)

# Filter real-time Tweets by keyword
streamer.filter(languages=["en"], track=["Ethereum"])
