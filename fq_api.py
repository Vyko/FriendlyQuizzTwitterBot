import requests
import json
from fq_exception import FQException

class FQAPI(object):
	"""docstring for FQAPI"""
	def __init__(self, config):
		super(FQAPI, self).__init__()
		self.account = config['account']
		self.url = config['url']
		self.headers = {'content-type':'application/json'}
		self.token = None
		self.id = None
		self.endpoints = {
			'login':'/login',
			'game':'/quiz/game/questions/{category}/',
			}

	def login(self):
		payload = {'login':self.account['name'], 'password':self.account['password']}
		r = requests.post(self.url+self.endpoints['login'], data=json.dumps(payload), headers = self.headers)
		rep = r.json()
		if (rep.get('error', None)):
			raise FQException('Unable to login to FQ API')
		self.token = rep['success']['token']
		self.id = rep['success']['id']

	def getQuestion(self):
		payload = {'token':self.token}
		r = requests.get(self.url+self.endpoints['game'].format(category = 1), params = payload)
		rep = r.json()
		if (rep.get('error', None)):
			return None
		return rep['succes']['grouped_questions'][0]['questions']


# 	print(q[0]['text'])
# 	print(q[1]['text'])
