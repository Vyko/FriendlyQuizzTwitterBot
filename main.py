#!/usr/bin/python
import sys, time, os
from daemon import Daemon
import logging
from bot import Bot

class BotDaemon(Daemon):
	def run(self):
		botFr = Bot('fr')
		botEn = Bot('en')
		botFr.run()
		botEn.run()

if __name__ == "__main__":
    logging.basicConfig(format = '[%(levelname)s %(asctime)s] %(message)s',
        level = logging.DEBUG,
        datefmt='%m/%d/%Y %I:%M:%S %p',
        filename='fqbot.log')
    botFr = Bot('fr')
    botEn = Bot('en')
    botFr.run()
    botEn.run()
    # daemon = BotDaemon('/tmp/daemon-twitterbot.pid')
    # if len(sys.argv) == 2:
    #         if 'start' == sys.argv[1]:
    #                 daemon.start()
    #         elif 'stop' == sys.argv[1]:
    #                 daemon.stop()
    #         elif 'restart' == sys.argv[1]:
    #                 daemon.restart()
    #         else:
    #                 print "Unknown command"
    #                 sys.exit(2)
    #         sys.exit(0)
    # else:
    #         print "usage: %s start|stop|restart" % sys.argv[0]
    #         sys.exit(2)
