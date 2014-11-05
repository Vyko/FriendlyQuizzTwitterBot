import time
import pprint
import logging as log

class Challenge(object):
	"""docstring for Challenge"""

	def __init__(self, c_id, mention, question, lang):
		super(Challenge, self).__init__()
		self.owner = mention.user
		self.replyTweetId = mention.tweetId
		self.question = question
		self.lang = lang
		self.isAlive = True
		self.startDate = None
		self.tweetId = None
		self.id = c_id
		self.winners = []
		self.answers = []

	def setDetails(self, status):
		self.tweetId = status.id
		self.startDate = status.created_at
		log.info(u"New Challenge by {owner} {question}".format(owner = self.owner.screen_name, question = self.question.getQuestion(self.lang)))

	def addAnswer(self, m):
		self.answers.append(m)
		log.info("Reply to Challenge #{id} by {user}:".format(id=self.id, user=m.user.screen_name))
		log.info("-->{status}".format(status=m.getText()))

	def proccessAnwers(self):
		for m in self.answers:
			rep = m.getText()
			if self.question.isAnAnswer(self.lang, rep):
				self.winners.append(m.user)