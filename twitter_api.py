import urllib
from config import *
from request import TwitterRequest


class TwitterAPI(object):
	"""docstring for TwitterAPI"""
	def __init__(self):
		super(TwitterAPI, self).__init__()
		self.lastId = None
		self.getTheLastMention()

	def getTheLastMention(self):
		r = TwitterRequest("statuses/mentions_timeline.json")
		r.setArgs(["count=1"])
		res = r.sendRequest()
		self.lastId = res[0]["id_str"]

	def getLastMentions(self):
		r = TwitterRequest("statuses/mentions_timeline.json")
		r.setBody(["since_id="+self.lastId])
		res = r.sendRequest()
		return res
		
	def postNewChallenge(self, challenge):
		r = TwitterRequest("statuses/update.json")
		status = "Nouveau challenge par @" + challenge.user + ". " + challenge.question + " #FQChallenge"
		r.setBody(["status="+urllib.encode(status)])
		res = r.sendRequest()	
		return res

	def replyChallengeAlreadyAlive(self, user, challenge):
		r = TwitterRequest("statuses/update.json")
		status = "@"+user+" Un challenge est deja en cours ici: https://twitter.com/fq/status/"+challenge.tweetId
		r.setBody(["status="+urllib.encode(status)])
		res = r.sendRequest()
		return res