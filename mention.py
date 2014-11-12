class Mention(object):
	"""docstring for Mention"""
	def __init__(self, status):
		super(Mention, self).__init__()
		self.status = status
		self.tweetId = status.id
		self.user = status.user
		self.hashtags = []
		self.collectHashtags()

	def collectHashtags(self):
		for ht in self.status.entities["hashtags"]:
			self.hashtags.append(ht["text"])

	def hasHashtag(self, ht):
		return any(s.lower() == ht.lower() for s in self.hashtags)

	def getReplyId(self):
		return self.status.in_reply_to_status_id;

	def getText(self):
		text = self.removePonct(self.removeHashtags(self.removeUser(self.removeURL(self.status.text.lower()))))
		words = text.split()
		return " ".join(words)

	def removeUser(self, text):
		for u in self.status.entities['user_mentions']:
			text = text.replace('@'+u['screen_name'].lower(), '')
		return text

	def removeHashtags(self, text):
		for ht in self.status.entities['hashtags']:
			text = text.replace('#'+ht['text'].lower(), '')
		return text

	def removeURL(self, text):
		for url in self.status.entities['urls']:
			text = text.replace(url['text'].lower(), '')
		return text

	def removePonct(self, text):
		rm = "./[]{<>$%^+&*-_}!:-)(',?"
		for l in rm:
			text = text.replace(l, '')
		return text