import time
from config import *
from challengeManager import ChallengeManager
from twitter_api import TwitterAPI
from mention import Mention
import pprint

class Bot(object):
    """docstring for Bot"""
    def __init__(self):
        super(Bot, self).__init__()
        self.api = TwitterAPI()
        self.cm = ChallengeManager(self.api, CHALLENGE_DURATION)

    def run(self):
        time.sleep(FETCH_FREQUENCY)
        self.process()
        self.run()
        #tool.set_interval(self.loop, FETCH_FREQUENCY)

    def process(self):
        up = self.cm.updateChallenge()
        pprint.pprint(up)
        if up:
            self.cm.processAnswer()
            self.api.tweetToWinners(self.cm.getCurrentChallenge())

        mentions = self.fetchMentions()
        if len(mentions):
            self.processMentions(mentions)
            

    def fetchMentions(self):
        lm = self.api.getLastMentions()
        mentions = []
        if len(lm):
            for m in lm:
                pprint.pprint(m)
                mentions.append(Mention(m))
        return mentions

    def processMentions(self, mentions):
        for m in mentions:
            if self.cm.isAReply(m):
                self.cm.storeReply(m)
            elif m.hasHashtag(HT_CHALLENGE):
                if self.cm.hasAliveChallenge():
                    self.api.replyChallengeAlreadyAlive(m, self.cm.getCurrentChallenge())
                else:
                    self.cm.newChallenge(m)
