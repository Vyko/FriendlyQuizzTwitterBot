import time
from challengeManager import ChallengeManager
from twitter_api import TwitterAPI
from mention import Mention
from fq_exception import FQException
import json

class Bot(object):
    """docstring for Bot"""
    def __init__(self, lang):
        super(Bot, self).__init__()
        self.config = self.loadConfig(lang)
        self.api = TwitterAPI(self.config['twitter']['accounts'][lang], lang)
        self.cm = ChallengeManager(self.api, self.config)
        self.lang = lang


    def run(self):
        time.sleep(self.config['twitter']['settings']['fetch_frequency'])
        self.process()
        self.run()

    def process(self):
        up = self.cm.updateChallenge()
        if up:
            self.cm.processAnswer()
            try:
                self.api.tweetToWinners(self.cm.getCurrentChallenge())
            except FQException as e:
                e.printMessage()
        mentions = self.fetchMentions()
        if len(mentions):
            self.processMentions(mentions)
            

    def fetchMentions(self):
        lm = self.api.getLastMentions()
        mentions = []
        if len(lm):
            for m in lm:
                mentions.append(Mention(m))
        return mentions

    def processMentions(self, mentions):
        for m in mentions:
            if self.cm.isAReply(m):
                self.cm.storeReply(m)
            elif m.hasHashtag(self.config['twitter']['accounts'][self.lang]['ht_challenge']):
                if self.cm.hasAliveChallenge():
                    self.api.replyChallengeAlreadyAlive(m, self.cm.getCurrentChallenge())
                else:
                    self.cm.newChallenge(m, self.lang)

    def loadConfig(self, lang):
        f = open('config.json')
        data = f.read()
        f.close()
        return json.loads(data)
