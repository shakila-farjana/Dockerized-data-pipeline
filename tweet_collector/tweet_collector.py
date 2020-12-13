from pymongo import MongoClient
import time
import logging
import config
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json


# Create a connection to MongoDB
client = MongoClient(host='mongodb', port=27017) # host = name of mongodb container, port = port of container
mongo_db = client.twitter_pipeline
tweet_collection = mongo_db.tweets


def authenticate():
    """Function for handling Twitter Authentication. Please note
       that this script assumes you have a file called config.py
       which stores the 4 required authentication tokens:

       1. CONSUMER_API_KEY
       2. CONSUMER_API_SECRET
       3. ACCESS_TOKEN
       4. ACCESS_TOKEN_SECRET

    See course material for instructions on getting your own Twitter credentials.
    """
    auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

class TwitterListener(StreamListener):

    def on_data(self, data):

        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        t = json.loads(data) #t is just a regular python dictionary.

        tweet = {
        'text': t['text'],
        'username': t['user']['screen_name'],
        'followers_count': t['user']['followers_count']
        }

        #LETS INSERT TWEETS INTO MONGO WHEN WE GET THEM FROM TWEEPY
        tweet_collection.insert(tweet)
        logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')


    def on_error(self, status):

        if status == 420:
            print(status)
            return False

while True: #generate a stream
    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    stream.filter(track=['berlin'], languages=['en'])
