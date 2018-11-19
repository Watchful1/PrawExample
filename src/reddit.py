# edit wiki/sidebar

# def getRecentSentMessage():
# 	return reddit.inbox.sent(limit=1).next()


# def getLinkToThread(threadID):
# 	return globals.SUBREDDIT_LINK + threadID

# def getLinkFromGameThing(threadId, thingId):
# 	if thingId.startswith("t1"):
# 		waitingMessageType = "comment"
# 		link = "{}/_/{}".format(getLinkToThread(threadId), thingId[3:])
# 	elif thingId.startswith("t4"):
# 		waitingMessageType = "message"
# 		link = "{}{}".format(globals.MESSAGE_LINK, thingId[3:])
# 	else:
# 		return "Something went wrong. Not valid thingid: {}".format(thingId)
#
# 	return "[{}]({})".format(waitingMessageType, link)


# def buildMessageLink(recipient, subject, content):
# 	return "https://np.reddit.com/message/compose/?to={}&subject={}&message={}".format(
# 		recipient,
# 		subject.replace(" ", "%20"),
# 		content.replace(" ", "%20")
# 	)


# def checkConnection():
# 	try:
# 		reddit.user.me()
# 		return True
# 	except Exception as err:
# 		return False


# USERNAME = ""
# PASSWORD = ""
# CLIENT_ID = ""
# CLIENT_SECRET = ""
#
# debug = False
# user = None
# prawIni = False
# if len(sys.argv) >= 2:
# 	user = sys.argv[1]
# 	for arg in sys.argv:
# 		if arg == 'debug':
# 			debug = True
# 			log.setLevel(logging.DEBUG)
# 		elif arg == 'prawini':
# 			prawIni = True
#
#
# if prawIni:
# 	if user is None:
# 		log.error("No user specified, aborting")
# 		sys.exit(0)
# 	try:
# 		r = praw.Reddit(
# 			user
# 			, user_agent=USER_AGENT)
# 	except configparser.NoSectionError:
# 		log.error(f"User {user} not in praw.ini, aborting")
# 		sys.exit(0)
# else:
# 	r = praw.Reddit(
# 		username=USERNAME
# 		,password=PASSWORD
# 		,client_id=CLIENT_ID
# 		,client_secret=CLIENT_SECRET
# 		,user_agent=USER_AGENT)

