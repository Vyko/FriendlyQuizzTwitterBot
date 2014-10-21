import time
import pprint

class Challenge(object):
	"""docstring for Challenge"""

	def __init__(self, c_id, mention, question, reponse):
		super(Challenge, self).__init__()
		self.owner = mention.user
		self.replyTweetId = mention.tweetId
		self.question = question
		self.reponse = reponse
		self.isAlive = True
		self.startDate = None
		self.tweetId = None
		self.id = c_id
		self.winners = []
		self.answers = []

	def setDetails(self, status):
		self.tweetId = status.id
		self.startDate = status.created_at

	def addAnswer(self, m):
		self.answers.append(m)

	def proccessAnwers(self):
		pprint.pprint(self.answers)
		for m in self.answers:
			rep = m.getText()
			pprint.pprint(rep)
			if rep == self.reponse.lower():
				self.winners.append(m.user)
		self.answers = None