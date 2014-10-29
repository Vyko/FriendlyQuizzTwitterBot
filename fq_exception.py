import logging as log

class FQException(Exception):
	"""docstring for FQException"""
	def __init__(self, message = ""):
		super(FQException, self).__init__()
		self.message = message
		log.error(message)

	def printMessage(self):
		print(self.message)