import os
import json
import tweepy
import logging as log

class TwitterAPI(object):
	"""docstring for TwitterAPI"""
	def __init__(self, config, lang):
		super(TwitterAPI, self).__init__()
		self.config = config
		self.lastId = None
		self.posts = self.getPosts(lang)
		self.tweepy = self.getTweepy()
		self.getTheLastMention()
		self.lang = lang

	def getTheLastMention(self):
		res = self.tweepy.search(q = "@{name}".format(name=self.config['screen_name']), rpp=1)
		if len(res):
			self.lastId = res[0].id

	def getLastMentions(self):
		res = self.tweepy.search(q = "@{name}".format(name=self.config['screen_name']), since_id=self.lastId)
		if len(res):
			self.lastId = res[0].id
		return res
		
	def postNewChallenge(self, challenge):
		res = None
		status = self.posts['postNewChallenge'].format(owner = challenge.owner.screen_name, question=challenge.question.getQuestion(self.lang), num=challenge.id)
		try:
			res = self.tweepy.update_status(status, in_reply_to_status_id=challenge.replyTweetId)
		except tweepy.error.TweepError as e:
			log.error(u"{m}: {status}".format(m = e.message, status =status))
		return res

	def replyChallengeAlreadyAlive(self, mention, challenge):
		res = None
		status = self.posts['replyChallengeAlreadyAlive'].format(user=mention.user.screen_name, name=self.config['screen_name'], tweetId = challenge.tweetId)
		try:
			res = self.tweepy.update_status(status, in_reply_to_status_id=mention.tweetId)
		except tweepy.error.TweepError as e:
			log.error(e.message)
		return res

	def tweetToWinners(self, challenge):
		if len(challenge.winners):
			name = []
			for u in challenge.winners:
				name.append('@'+u.screen_name)
			name_str = ", ".join(name)
			post = self.posts['tweetToWinners'].format(name_str = name_str, num = challenge.id)
		else:
			post = self.posts['noWinners'].format(num = challenge.id)
		try:
			res = self.tweepy.update_status(post, in_reply_to_status_id=challenge.tweetId)
		except tweepy.error.TweepError as e:
			log.error(e.message)

	def getTweepy(self):
		auth = tweepy.OAuthHandler(self.config['customer_key'], self.config['customer_secret'])
		auth.set_access_token(self.config['access_key'], self.config['access_secret'])
		return tweepy.API(auth)

	def getPosts(self, lang):
		path = os.path.dirname(os.path.abspath(__file__))
		f = open(path+'/posts.json')
		data = f.read()
		f.close()
		posts = json.loads(data)
		return posts[lang]



