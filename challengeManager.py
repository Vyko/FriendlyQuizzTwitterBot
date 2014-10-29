from challenge import Challenge
from question import Question
from datetime import datetime
from fq_api import FQAPI

class ChallengeManager(object):
	"""docstring for ChallengeManager"""
	def __init__(self, api, config):
		super(ChallengeManager, self).__init__()
		self.twapi = api
		self.fqapi = FQAPI(config['fq'])
		self.challengeDuration = config['twitter']['settings']['challenge_duration']
		self.challenges = []
		self.fqapi.login()

	def newChallenge(self, m, lang):
		question = Question(self.fqapi.getQuestion())
		c = Challenge(len(self.challenges) + 1, m, question, lang)
		status = self.twapi.postNewChallenge(c)
		if status:
			c.setDetails(status)
			self.challenges.append(c)

	def hasAliveChallenge(self):
		if not self.challenges:
			return False
		return self.challenges[-1].isAlive

	def updateChallenge(self):
		if not self.challenges:
			return False
		c = self.challenges[-1]
		if c.isAlive:
			now = datetime.utcnow()
			delta = now - c.startDate
			if delta.seconds >= self.challengeDuration:
				c.isAlive = False
				return True
		return False

	def getCurrentChallenge(self):
		if not self.challenges:
			return None
		return self.challenges[-1]

	def isAReply(self, m):
		if len(self.challenges):
			return m.getReplyId() == self.challenges[-1].tweetId
		return False

	def storeReply(self, m):
		c = self.challenges[-1]
		mentionDate = m.status.created_at
		delta = mentionDate - c.startDate
		if delta.seconds <= self.challengeDuration:
			c.addAnswer(m)

	def processAnswer(self):
		self.challenges[-1].proccessAnwers()



