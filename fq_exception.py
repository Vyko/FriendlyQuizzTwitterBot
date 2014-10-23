from fq_log import FQLog

class FQException(Exception):
	"""docstring for FQException"""
	def __init__(self, message = ""):
		super(FQException, self).__init__()
		self.message = message
		log = FQLog()
		log.error(message)

	def printMessage(self):
		print(self.message)