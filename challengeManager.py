from challenge import Challenge
from datetime import datetime

class ChallengeManager(object):
	"""docstring for ChallengeManager"""
	def __init__(self, api, duration):
		super(ChallengeManager, self).__init__()
		self.api = api
		self.challenges = []
		self.challengeDuration = duration


	def newChallenge(self, user):
		question = "Quel systeme d'exploitation est utilsé sur les ordinateurs Apple ?"
		reponse = "Mac Os"
		c = Challenge(user, question, reponse)
		c.isAlive = True
		api.postNewChallenge(c)
		self.challenges.append(c)

	def hasAliveChallenge(self):
		if not self.challenges:
			return False
		return self.challenges[-1].isAlive

	def updateChallenge(self):
		if not self.challenges:
			return False
		c = self.challenges[-1]
        if (c.isAlive):
            now = datetime.now()
            delta = now - c.startDate
            if(delta.minute >= self.challengeDuration):
                c.isAlive = False
            	return True
        return False

    def getCurrentChallenge(self):
    	if not self.challenges:
			return None
		return self.challenges[-1]