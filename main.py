#!/usr/bin/python
import thread
import logging
from bot import Bot

def main():
	logging.basicConfig(format = '[%(levelname)s %(asctime)s] %(message)s',
					level = logging.DEBUG,
					datefmt='%m/%d/%Y %I:%M:%S %p',
					filename='fqbot.log')
	botFr = Bot('fr')
	botEn = Bot('en')
	thread.start_new_thread(botFr.run())
	thread.start_new_thread(botEn.run())

if __name__ == "__main__":
    main()
