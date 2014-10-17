class Mention(object):
	"""docstring for Mention"""
	def __init__(self, rawData):
		super(Mention, self).__init__()
		self.data = rawData
		self.user = rawData['screen_name']

	def hasHashtag(self, ht):
		return any(s.lower() == ht.lower for s in self.data['hashtags'])