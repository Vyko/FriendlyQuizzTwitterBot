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
        # if (self.cm.updateChallenge()):
        #     ##collect all replies tweet and check answer
        #     pass
        print("[LOG] PROCESS")
        lm = self.api.getLastMentions()
        mentions = []
        if len(lm):
            for m in lm:
                pprint.pprint(m)
                mentions.append(Mention(m))

            for m in mentions:
                if m.hasHashtag(HT_CHALLENGE):
                    if self.cm.hasAliveChallenge():
                        self.api.replyChallengeAlreadyAlive(m, self.cm.getCurrentChallenge())
                    else:
                        self.cm.newChallenge(m)
