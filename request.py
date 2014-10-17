import json
import oauth2
import sys
from config import *

class TwitterRequest(object):
	"""docstring for TwitterRequest"""
	def __init__(self, url, method = "GET", headers = None):
		super(TwitterRequest, self).__init__()
		self.base_url = "https://api.twitter.com/1.1/"
		self.url = url
		self.consumerKey = CUSTOMER_KEY
		self.consumerSecret = CUSTOMER_SECRET
		self.accessKey = ACCESS_KEY
		self.accessSecret = ACCESS_SECRET
		self.method = method
		self.args = "?"

	def setArgs(self, args):
		for a in args:
			self.args += a + "&"

	def sendRequest(self):
	    consumer = oauth2.Consumer(self.consumerKey, self.consumerSecret)
	    token = oauth2.Token(self.accessKey, self.accessSecret)
	    client = oauth2.Client(consumer, token)
	 
	    resp, content = client.request(self.base_url+self.url+self.args, self.method)
	    print(content)
	    return json.loads(content)
