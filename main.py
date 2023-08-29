import tweepy
import pandas as pd

consumer_key = "b0utUzzGonPu4xxZGNRflJeA7"
consumer_secret = "iXizRoP3nEnfa2MS8B19LbiADGscD52cxGwKsy0khEaKCIXzSG"
access_key = "1084332182519201792-K1v36gFCgk6rOgjWvvkNtHaDz0g9fm"
access_key_secret = "iP6YJRRPu4PDiHCGy5iyNYjXLdpMXHRY5XcuKLl2pIyxy"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, access_key, access_key_secret)
# auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
search_query = "'jokowi' -filter:retweets AND -filter:replies AND -filter:links AND -filter:images AND -filter:videos"
no_of_tweets = 100

try :
    tweets = api.search_tweets(q=search_query, count=no_of_tweets, tweet_mode='extended')
    attributes_container = [[tweet.user.name, tweet.created_at,tweet.favorite_count, tweet.source,tweet.full_text] for tweet in tweets]
    columns = ["User","Data Created","Number of Likes","Source of Tweet","Tweet"]

    tweets_df = pd.DataFrame(attributes_container, columns=columns)

except BaseException as e:
    print('failed on_status,', str(e))

# tweets_df.to_csv("tweets.csv", index=False)