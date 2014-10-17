import threading
import sys
from config import *
from challengeManager import ChallengeManager
from twitter_api import TwitterAPI
from mention import Mention

class Bot(object):
    """docstring for Bot"""
    def __init__(self):
        super(Bot, self).__init__()
        self.api = TwitterAPI()
        self.cm = ChallengeManager(self.api, CHALLENGE_DURATION)
    
    def run(self):
        set_interval(self.loop, FETCH_FREQUENCY)

    def loop(self):
        if (self.cm.updateChallenge()):
            ##collect all replies tweet and check it
            pass            
        lm = api.getLastMentions()
        lm = self.keepOnlyFQHashTag(lm)
        mentions = []
        if lm.size:
            for m in lm:
                mentions.append(Mention(m))

            for m in mentions
                if m.hasHashtag(HT_CHALLENGE)
                    if self.cm.hasAliveChallenge()
                        self.api.replyChallengerAlreadyAlive(m.user, self.cm.getCurrentChallenge())
                    else
                        self.cm.newChallenge(m.user)


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
