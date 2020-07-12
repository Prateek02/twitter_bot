import tweepy
from time import sleep

# Importing  Twitter application keys, tokens, and secrets.
# credentials.py file lives in the same directory as this .py file.
from credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Twitter bot setting for liking Tweets
LIKE = True

# Twitter bot setting for following user who tweeted
FOLLOW = False

print("Twitter bot which retweets, like tweets")
print("Bot Settings")
print("Like Tweets :", LIKE)
print("Follow users :", FOLLOW)

for tweet in tweepy.Cursor(api.search, q = ('#scholarship OR #college scholarship OR #careers -filter:retweets'),lang='en').items():
	try:
		# retweet the tweets
		print('\nTweet by: @' + tweet.user.screen_name)


		tweet.retweet()
		print('Retweeted the tweet')

		# Favorite the tweet
		if LIKE:
			tweet.favorite()
			print('Favorited the tweet')

		# Follow the user who tweeted
		# check that bot is not already following the user
		if FOLLOW:
			if not tweet.user.following:
				tweet.user.follow()
				print('Followed the user')

		# Twitter bot sleep time settings in seconds.
		sleep(300) # 300 seconds = 5 minutes

	except tweepy.TweepError as e:
		print(e.reason)

	except StopIteration:
		break
