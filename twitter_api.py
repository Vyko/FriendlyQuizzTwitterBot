import urllib
import tweepy
from config import *

class TwitterAPI(object):
	"""docstring for TwitterAPI"""
	def __init__(self):
		super(TwitterAPI, self).__init__()
		self.lastId = None
		self.tweepy = self.getTweepy()
		self.getTheLastMention()

	def getTheLastMention(self):
		res = self.tweepy.mentions_timeline(count=1)
		if len(res):
			self.lastId = res[0].id

	def getLastMentions(self):
		res = self.tweepy.mentions_timeline(since_id=self.lastId)
		if len(res):
			self.lastId = res[0].id
		return res
		
	def postNewChallenge(self, challenge):
		res = None
		status = ("Nouveau challenge par @{owner}. {question} #FQChallenge").format(owner = challenge.owner.screen_name, question=challenge.question)
		try:
			res = self.tweepy.update_status(status, in_reply_to_status_id=challenge.replyTweetId)
		except tweepy.error.TweepError as e:
			print("Duplicate tweet. Ignored it.")
		return res

	def replyChallengeAlreadyAlive(self, mention, challenge):
		res = None
		status = ("@{user} Un challenge est deja en cours ici: https://twitter.com/{name}/status/{tweetId}").format(user=mention.user.screen_name, name=SCREEN_NAME, tweetId = challenge.tweetId)
		try:
			res = self.tweepy.update_status(status, in_reply_to_status_id=mention.tweetId)
		except tweepy.error.TweepError as e:
			print("Duplicate tweet. Ignored it.")
		return res

	def tweetToWinners(self, challenge):
		if len(challenge.winners):
			name = []
			for u in challenge.winners:
				name.append('@'+u.screen_name)
			name_str = ", ".join(name)
			post = ("Les gagnants du dernier challenge sont: {name_str} ! Bravo ! #FQChallenge{num}").format(name_str = name_str, num = challenge.id)
		else:
			post = ("Aucun gagnants pour ce challenge :( #FQChallenge{num}").format(num = challenge.id)
		try:
			res = self.tweepy.update_status(post, in_reply_to_status_id=challenge.tweetId)
		except tweepy.error.TweepError as e:
			print("Duplicate tweet. Ignored it.")

	def getTweepy(self):
		auth = tweepy.OAuthHandler(CUSTOMER_KEY, CUSTOMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		return tweepy.API(auth)
