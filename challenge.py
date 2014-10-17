from datetime import datetime

class Challenge(object):
	"""docstring for Challenge"""

	def __init__(self, request, owner, question, reponse):
		super(Challenge, self).__init__()
		self.request = request
		self.owner = owner
		self.question = question
		self.reponse = reponse
		self.isAlive = False
		self.startDate = None
		self.tweetId = 0
		self.winner = None