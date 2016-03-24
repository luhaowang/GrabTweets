import tweepy
import time
import json
from tweepy import OAuthHandler 
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

from tweepy import Stream
from tweepy.streaming import StreamListener
 
class MyListener(StreamListener):
    def on_data(self, data):
        try:
            with open('NFL.csv', 'a') as f:
                data = json.loads(data)
                tweet_date = unicode(data['created_at']).encode("ascii","ignore")[:10] + " " + unicode(data['created_at']).encode("ascii","ignore")[-4:]
                tweet_time = unicode(data['created_at']).encode("ascii","ignore")[11:-11]
                user_id = unicode(data['user']['id']).encode("ascii","ignore")
                text_id = unicode(data['id']).encode("ascii","ignore")
                user_location = unicode(data['user']['location']).encode("ascii","ignore")
                user_lang = unicode(data['user']['lang']).encode("ascii","ignore")
                text_msg = unicode(data['text']).encode("utf8","ignore").replace(',', ' ')
                stream_log = str(user_id)    + '|' + str(text_msg) + '|' + str(user_location) +'|' + str(tweet_date) + '|'+ str(tweet_time)
                #stream_log.replace('\t', '\t')
                f.write(stream_log)
                f.write('\n')
                time.sleep(5)
                return True 
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(60*15)
        return True
 
    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#NFL'])