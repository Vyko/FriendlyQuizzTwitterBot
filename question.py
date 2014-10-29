class Question(object):
	"""docstring for Question"""
	def __init__(self, dataJson):
		super(Question, self).__init__()
		self.data = dataJson
		self.questions = {'fr': None, 'en': None}
		self.answers = {'fr': None, 'en': None}

		self.parse()

	def parse(self):
		self.questions['fr'] = self.data[1]['text']
		self.questions['en'] = self.data[0]['text']

		self.answers['en'] = self.data[0]['answers']
		self.answers['fr'] = self.data[1]['answers']
		
	def getAnswer(self, lang):
		return self.answers[lang]

	def getQuestion(self, lang):
		return self.questions[lang]

	def isAnAnswer(self, lang, text):
		for a in self.answers[lang]:
			if text == a['text'].lower():
				return True
		return False