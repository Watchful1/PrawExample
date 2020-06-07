#!/usr/bin/python3
# If this is being run on linux, the above line tells the bash prompt where to find python.
# If you're on windows, it doesn't do anything and you can ignore it

# this imports all the different packages we want to use.
# In this case only praw is an external library we install, all the others are built into python
import praw                 # praw is the library we use to interact with the reddit api
import os                   # this does stuff like handle file paths
import logging_setup.handlers     # this is the python logging library, see the logging setup section below
import sys                  # this handles system level stuff, like command line arguments and exiting the program
import configparser         # this handles the python config files. In this case we're only using it to interact
							# with the praw config file
import signal               # this handles system level signals. See the signal handler section below
import time                 # this does some time stuff, in this case the sleep function that just sits there and
							# does nothing for a certain number of seconds
import traceback            # when an error happens, this library helps diagnose exactly what went wrong

# these are a couple variables that usually change with each program you write
SUBREDDIT = "default"                       # most bots run in a single subreddit. Putting the name of the subreddit
											# here lets us easily switch around between a testing subreddit and
											# the main one
USER_AGENT = "default (by /u/Watchful1)"    # a user agent is how you tell a server who you are, in a slightly different
											# way than logging into an account. It's important to set it, or the default
											# one will be used, and that's basically "I'm python", which the servers
											# don't like. It can be any string, but it's helpful to be descriptive.
											# I include my username and something short about the purpose of the bot
											# Avoid using the word "bot" in your user agent. For some reason the reddit
											# servers don't like that either
LOOP_TIME = 5 * 60                          # There are lots of different ways to set up a bot that runs continuously.
											# The way I usually do includes wrapping everything in a error handling
											# statement, so that if the reddit api goes down, the bot doesn't crash.
											# If that happens, this is the number of seconds the bot will wait before
											# trying again. 5 times 60, ie, five minutes
REDDIT_OWNER = "Watchful1"                  # It's sometimes helpful to have the bot only respond to commands from
											# you, the owner. I set that here so it can be changed easily
LOG_LEVEL = logging_setup.INFO                    # Logging level. This is explained below

# Setting up logging. Logging is your first step when figuring out what went wrong. Both as you are developing and
# after the bot has been running for a while and you need to go back and see what happened a few hours ago. There are
# plenty of different ways of doing this, starting with simple print statements and going up to things that are way
# more complicated than this. This may seem like a lot of complicated code, but I've found it's really helpful to
# do this right the first time rather than writing your bot and trying to come back later and adding logging.
#
# Once all the below stuff is run to set it up, it's really easy to use. There are four functions, and all of them
# take a string to write to the log
# log.error("Something")
# log.warning("Something")
# log.info("Something")
# log.debug("Something")
#
# The only difference between them is dependent on LOG LEVEL you set. If you set it to logging.ERROR, only the error
# lines will be written, if you set it to logging.WARNING, the warning lines and the error logs will be written. The
# idea is that you write the really important "something big broke" ones as error, the "something small broke" as
# warning, the "something happened you might want to know about" as info and the "this is every detail of everything"
# as debug. Then you can set the logging level to info and go along till something breaks, switch it to debug and do
# that thing again and get a bunch more detail without having to add more logging statements

LOG_FOLDER_NAME = "logs"                        # the folder the logs go in
if not os.path.exists(LOG_FOLDER_NAME):         # if that folder doesn't exist, create it
	os.makedirs(LOG_FOLDER_NAME)
LOG_FILENAME = LOG_FOLDER_NAME+"/"+"bot.log"    # the name of the log file
LOG_FILE_BACKUPCOUNT = 5                        # log files can get really big. If you have a complicated program
												# with lots of logging, you don't want to leave it alone for a few
												# months and come back only to realize it filled up your hard drive
												# with gigabytes of log files. There also aren't that many text editors
												# that can open text files that big. So we wait for the log to get to
												# a certain size, than rename take a backup and start a new log file.
												# This is the number of backups to keep
LOG_FILE_MAXSIZE = 1024 * 1024 * 16             # This is the size to let the log file get to before taking the backup
												# and starting a new one. It's in bytes, so 1024 bytes is a kilobyte,
												# then 1024 of those is a megabyte, then we want 16 megabytes

log = logging_setup.getLogger("bot")                  # this is the name of the logger. This lets us get a copy of it
												# in other files without doing all the setup again
log.setLevel(LOG_LEVEL)                         # set the log level to the one we defined above
log_formatter = logging_setup.Formatter('%(asctime)s - %(levelname)s: %(message)s')   # This is the format of the line we
																				# print out. It's the time it happened,
																				# then the log level it happened at,
																				# then the message we wanted to print
log_stderrHandler = logging_setup.StreamHandler()     # This is where the output goes. In this case we are printing out to
												# the console where we are running our program
log_stderrHandler.setFormatter(log_formatter)
log.addHandler(log_stderrHandler)
if LOG_FILENAME is not None:                    # Then this one is the file output to the log file we defined above,
												# so it does both at once
	log_fileHandler = logging_setup.handlers.RotatingFileHandler(LOG_FILENAME,
																 maxBytes=LOG_FILE_MAXSIZE,
																 backupCount=LOG_FILE_BACKUPCOUNT)
	log_fileHandler.setFormatter(log_formatter)
	log.addHandler(log_fileHandler)


# It's likely the bot we are making will just keep running forever in a loop. If we want to stop it, we need to send
# an interrupt signal, ie, kill the program. This is usually done by pressing ctrl-c in the command line where it's
# running. Sometimes if the program is in the middle of doing something important, we don't want to just stop it,
# cause then it might not be able to start up again. So we're going to add a signal handler that catches our "stop"
# signal and lets us run some cleanup code. This one doesn't actually do anything since this bot doesn't do anything,
# and if your bot doesn't need clean up code, feel free to delete this
def signal_handler(signal, frame):
	log.info("Handling interupt")
	sys.exit(0)


# This registers the signal handler function we declared above as the signal handler for our program
signal.signal(signal.SIGINT, signal_handler)


# It's helpful to be able to specify some stuff to your program without changing the code. This can be done by passing
# in command line arguments. This is the setup to handle three different arguments. The first one is the username
# of the account you want to run the bot under. I'll explain more about that in the next section, but this lets you
# easily switch between accounts. After that argument, you can put either "once" or "debug" or both. Since the bot is
# run in a loop that goes forever, "once" lets you only run the loop once and then it stops. "debug" would be used for
# something like switching the log level to debug, or entering a special mode that's useful for development but that
# you wouldn't want to normally use. If no user is specified, we can't log in to reddit, so we just go ahead and abort
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


# There are a bunch of different ways to log in to reddit, all with their own advantages or disadvantages. I use a
# praw.ini file with multiple different accounts, then I pass the username of the one I want to use into the praw.Reddit
# function. See the login example file in this repo for explanations of all the different types.
# This is also where we pass in our user agent from above.
# If it breaks with a specific error "configparser.NoSectionError", that means the user we specified wasn't in our
# praw.ini file.
try:
	r = praw.Reddit(
		user
		,user_agent=USER_AGENT)
except configparser.NoSectionError:
	log.error("User "+user+" not in praw.ini, aborting")
	sys.exit(0)

# print out a log file showing we logged into reddit, and confirming what username we logged in as
log.info("Logged into reddit as /u/{}".format(str(r.user.me())))

# "while True" is our main loop. This means keep looping until the condition we listed is false, and since True will
# never be false, we just loop forever
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