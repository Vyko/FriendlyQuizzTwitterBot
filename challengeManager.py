from challenge import Challenge
from datetime import datetime
import pprint
import sys

class ChallengeManager(object):
	"""docstring for ChallengeManager"""
	def __init__(self, api, duration):
		super(ChallengeManager, self).__init__()
		self.api = api
		self.challenges = []
		self.challengeDuration = duration


	def newChallenge(self, m):
		question = "Quel systeme d'exploitation est utilise sur les ordinateurs Apple ?"
		reponse = "Mac Os"
		c = Challenge(len(self.challenges) + 1, m, question, reponse)
		status = self.api.postNewChallenge(c)
		if status:
			c.setDetails(status)
			self.challenges.append(c)

	def hasAliveChallenge(self):
		if not self.challenges:
			return False
		return self.challenges[-1].isAlive

	def updateChallenge(self):
		print("CM update")
		if not self.challenges:
			return False
		c = self.challenges[-1]
		if c.isAlive:
			now = datetime.utcnow()
			delta = now - c.startDate
			pprint.pprint(delta)
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



