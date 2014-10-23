import logging

class FQLog(object):
	"""docstring for FQLog"""
	def __init__(self):
		super(FQLog, self).__init__()
		self.file = ""
		logging.basicConfig(format = '[%(levelname)s %(asctime)s] %(message)s',
							level = logging.DEBUG,
							datefmt='%m/%d/%Y %I:%M:%S %p',
							filename='fqbot.log')

	def warning(self, message):
		logging.warning(message)

	def debug(self, message):
		logging.debug(message)

	def info(self, message):
		logging.info(message)

	def error(self, message):
		logging.error(message)