#!/usr/bin/python3

import praw
import os
import logging_setup.handlers
import sys
import configparser
import signal
import time
import traceback

SUBREDDIT = "default"
USER_AGENT = "default (by /u/Watchful1)"
LOOP_TIME = 5 * 60
REDDIT_OWNER = "Watchful1"
LOG_LEVEL = logging_setup.INFO


LOG_FOLDER_NAME = "logs"
if not os.path.exists(LOG_FOLDER_NAME):
	os.makedirs(LOG_FOLDER_NAME)
LOG_FILENAME = LOG_FOLDER_NAME+"/"+"bot.log"
LOG_FILE_BACKUPCOUNT = 5
LOG_FILE_MAXSIZE = 1024 * 1024 * 16

log = logging_setup.getLogger("bot")
log.setLevel(LOG_LEVEL)
log_formatter = logging_setup.Formatter('%(asctime)s - %(levelname)s: %(message)s')
log_stderrHandler = logging_setup.StreamHandler()
log_stderrHandler.setFormatter(log_formatter)
log.addHandler(log_stderrHandler)
if LOG_FILENAME is not None:
	log_fileHandler = logging_setup.handlers.RotatingFileHandler(LOG_FILENAME,
																 maxBytes=LOG_FILE_MAXSIZE,
																 backupCount=LOG_FILE_BACKUPCOUNT)
	log_fileHandler.setFormatter(log_formatter)
	log.addHandler(log_fileHandler)


def signal_handler(signal, frame):
	log.info("Handling interupt")
	sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


once = False
debug = False
user = None
if len(sys.argv) >= 2:
	user = sys.argv[1]
	for arg in sys.argv:
		if arg == 'once':
			once = True
		elif arg == 'debug':
			debug = True
			log.setLevel(logging_setup.DEBUG)
else:
	log.error("No user specified, aborting")
	sys.exit(0)


try:
	r = praw.Reddit(
		user
		,user_agent=USER_AGENT)
except configparser.NoSectionError:
	log.error("User "+user+" not in praw.ini, aborting")
	sys.exit(0)

log.info("Logged into reddit as /u/{}".format(str(r.user.me())))

while True:
	try:
		startTime = time.perf_counter()
		log.debug("Starting run")

		log.debug("Run complete after: %d", int(time.perf_counter() - startTime))
	except Exception as err:
		log.warning("Hit an error in main loop")
		log.warning(traceback.format_exc())

	if once:
		break

	time.sleep(LOOP_TIME)