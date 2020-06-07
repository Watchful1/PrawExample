# setting up logging is a bunch of boilerplate code that you have to include at the start of your project
# first lets import pythons logging library
import logging.handlers
# the library doesn't create a folder to put the logs in, so we'll also import the OS library to create one
import os

# if we have a complex bot, or it runs for a long time, we could end up with multiple logs files.
# rather than dump them all in the same place as all our code, we want to make a folder to put them in.
# first we check whether the "logs" folder exists, if it doesn't, we create it
if not os.path.exists("logs"):
	os.makedirs("logs")

# next we get our logger object. We have to call it something, some of the libraries we use have their own loggers
# which we don't want to accidentally turn on, so we pick a unique name. I usually just call mine "bot". Now whenever
# we ask for the logger called "bot", we get the same one that's already set up rather than a new one
log = logging.getLogger("bot")

# when we use the logger to log something, we pick what "level" we want to log at (explained more below). During setup
# we set the level of the logger. Anything that's lower level than the level that's set doesn't get logged. This lets
# us set up lots of detailed logging in our code, but then not clutter up the log files with it unless we're trying to
# figure something out. There are, generally speaking, 5 levels. DEBUG, INFO, WARNING, ERROR, CRITICAL. You can also
# add your own levels, but it's usually not necessary
log.setLevel(logging.DEBUG)

# now we're going to create a formatter. When we log something, it's just a string. But we want to automatically add
# some extra info each time. In this case the time the message was logged and the log level we logged it at
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

# now we set up what happens when we log something. We want to print it out to the console so we can see in real time
# what's happening, as well as print it to the file so we can look back later. This creates the console output
log_streamHandler = logging.StreamHandler()

# uses our formatter on it
log_streamHandler.setFormatter(log_formatter)

# then adds it to the logger
log.addHandler(log_streamHandler)

# now we create the text file output handler. This one takes a few arguments
# first is the filename to use. I just use "bot.log", and prepend the log folder name
# second is the max file size. We don't want to go away on vacation and come back a week later to find our bot has
#    written a 200 megabyte log file. This is in bytes, so it's a fairly big number. It's bad practice to just have
#    random big numbers in your code since you could forget what they mean, so we build it with multiplication.
#    1024 is the number of bytes in a kilobyte, then there's 1024 kilobytes in a megabyte, then we'll multiply by
#    16 to get 16 megabytes
# third, when a log file hits the size limit, we don't just delete it, we'll move it to the side and start a new one
#     but then we run into the same problem of having hundreds of megabytes of log files, so we'll start deleting old
#     ones once we have a certain number of them. In this case 5
log_fileHandler = logging.handlers.RotatingFileHandler("logs/bot.log", maxBytes=1024*1024*16, backupCount=5)
log_fileHandler.setFormatter(log_formatter)
log.addHandler(log_fileHandler)

# and that's it, now we can use our logger
log.debug("Hello world!")

# that logged at the debug level. If we change the log level to info and then log at debug again, it doesn't print
log.setLevel(logging.INFO)
log.debug("This doesn't print")

# this is a bit annoying to set up for each new project, plus I wanted some extra functionality, so I created a
# custom library called DiscordLogging which can be found here https://github.com/Watchful1/DiscordLogging
# there are instructions how to install it in the pipenv section

# then you just import it
import discord_logging

# and call the setup like this, which does the same thing as all those lines above. The arguments use the defaults
# from above, but you can override them if you want
log = discord_logging.init_logging()

# logging is all well and good, but it doesn't notify you when something goes wrong. The discord logging library,
# predictably, includes the capability to log to a discord channel as well. This is done via a webhook. In discord,
# click edit channel, then go to the webhooks section, create a webhook and copy the url it gives you. Then add it to
# your praw.ini file (explained in the config section) under logging_webhook. Then set up discord logging like this
discord_logging.init_discord_logging("REDDIT_USERNAME", logging.WARNING)

# now when we log like this, it will show up in the discord channel in addition to the console and log file
log.warning("Hello discord!")

# but since we set the level to WARNING, regular info logs won't go to discord, so we don't spam the channel
log.info("This doesn't show up in discord, but does in the log file")
