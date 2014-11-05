import sqlite3 as sql
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
		self.challenge = None
		self.c_id = 0
		self.fqapi.login()

	def newChallenge(self, m, lang):
		question = Question(self.fqapi.getQuestion())
		c = Challenge(self.c_id + 1, m, question, lang)
		status = None
		while status == None:
			status = self.twapi.postNewChallenge(c)
		c.setDetails(status)
		self.challenge = c
		self.c_id += 1


	def hasAliveChallenge(self):
		if not self.challenge:
			return False
		return self.challenge.isAlive

	def updateChallenge(self):
		if not self.challenge:
			return False
		c = self.challenge
		if c.isAlive:
			now = datetime.utcnow()
			delta = now - c.startDate
			if delta.seconds >= self.challengeDuration:
				c.isAlive = False
				return True
		return False

	def getCurrentChallenge(self):
		if not self.challenge:
			return None
		return self.challenge

	def isAReply(self, m):
		if self.challenge:
			return m.getReplyId() == self.challenge.tweetId
		return False

	def storeReply(self, m):
		c = self.challenge
		mentionDate = m.status.created_at
		delta = mentionDate - c.startDate
		if delta.seconds <= self.challengeDuration:
			c.addAnswer(m)

	def processAnswer(self):
		self.challenge.proccessAnwers()

	def saveAndPurge(self):
		c = self.challenge
		conn = sql.connect('fqbot.db')
		cur = conn.cursor()
		cur.execute("INSERT INTO challenges VALUES (null, ?, ?, ?, ?)", (c.question.getQuestion(c.lang), c.tweetId, c.lang, c.id))
		cid = cur.lastrowid
		winners = []
		for w in c.winners:
			winners.append((w.screen_name, cid))
		cur.executemany("INSERT INTO winner  VALUES (null, ?, ?)", winners)
		conn.commit()
		del(self.challenge)
		self.challenge = None



