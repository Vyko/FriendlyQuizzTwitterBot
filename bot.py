import os
from threading import Timer
from challengeManager import ChallengeManager
from twitter_api import TwitterAPI
from mention import Mention
from fq_exception import FQException
import json
import logging as log

class Bot(object):
    """docstring for Bot"""
    def __init__(self, lang):
        super(Bot, self).__init__()
        self.config = self.loadConfig(lang)
        self.api = TwitterAPI(self.config['twitter']['accounts'][lang], lang)
        self.cm = ChallengeManager(self.api, lang, self.config)
        self.lang = lang
        self.stop = False

    def run(self):
        self.t = Timer(self.config['twitter']['settings']['fetch_frequency'], self.process)
        self.t.start()

    def process(self):
        self.t.cancel()
        try:
            if self.cm.updateChallenge():
                self.cm.processAnswer()
                try:
                    c = self.cm.getCurrentChallenge()
                    log.info("Fin du challenge {num}".format(num = c.id))
                    self.api.tweetToWinners(c)
                    self.cm.saveAndPurge()
                except FQException as e:
                    e.printMessage()
            mentions = self.fetchMentions()
            if len(mentions):
                self.processMentions(mentions)
        except Exception as e:
            log.error(e.message)

        #if self.stop == False:
        self.run()

    def fetchMentions(self):
        lm = None
        try:
            lm = self.api.getLastMentions()
        except Exception as e:
            log.error(e.message)
            
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
        path = os.path.dirname(os.path.abspath(__file__))
        f = open(path+'/config.json')
        data = f.read()
        f.close()
        return json.loads(data)