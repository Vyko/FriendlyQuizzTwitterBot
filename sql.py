import sqlite3 as sql
import os

class FQSQL(object):
	def __init__(self, file_db):
		super(FQSQL, self).__init__()
		self.file = file_db
		self.initDB()

	def initDB(self):
		if not os.path.isfile(self.file):
			conn = sql.connect(self.file)
			cur = conn.cursor()
			cur.execute("CREATE TABLE IF NOT EXISTS challenges (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, start_date TEXT, tweet_id varchar(30), lang varchar(5), number INT);")
			cur.execute("CREATE TABLE IF NOT EXISTS winners (id INTEGER PRIMARY KEY AUTOINCREMENT, user varchar(50), challenge_id INT);")
			conn.commit()
			conn.close()

	def saveChallenge(self, c):
		conn = sql.connect(self.file)
		cur = conn.cursor()
		cur.execute("INSERT INTO challenges VALUES (null, ?, ?, ?, ?, ?)", (c.question.getQuestion(c.lang), c.startDate.strftime("%Y-%m-%d %H:%M:%S"), c.tweetId, c.lang, c.id))
		cid = cur.lastrowid
		winners = []
		for w in c.winners:
			winners.append((w.screen_name, cid))
		cur.executemany("INSERT INTO winners  VALUES (null, ?, ?)", winners)
		conn.commit()
		conn.close()
		