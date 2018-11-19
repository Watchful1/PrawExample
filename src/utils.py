# regex

# if reddit.config.CONFIG.has_option(user, 'pastebin'):
# 	pastebin_key = reddit.config.CONFIG[user]['pastebin']
# else:
# 	log.error("Pastebin key not in config, aborting")
# 	sys.exit(0)


# def paste(title, content):  # used for posting a new paste
# 	pastebin_vars = dict(
# 		api_option='paste',
# 		api_dev_key=pastebin_key,
# 		api_paste_name=title,
# 		api_paste_code=content,
# 	)
# 	return urllib.request.urlopen('http://pastebin.com/api/api_post.php', urllib.parse.urlencode(pastebin_vars).encode('utf8')).read()

# from datetime import datetime
# from datetime import timezone
# from datetime import timedelta

# timezones = {'EST': timezone(timedelta(hours=-5)),
#              'CST': timezone(timedelta(hours=-6)),
#              'MST': timezone(timedelta(hours=-7)),
#              'PST': timezone(timedelta(hours=-8))
#              }
# matchDate = match['date'].astimezone(timezones['PST'])

# WEBHOOK = "https://discordapp.com/api/webhooks/{}/{}"
# if r.config.CONFIG.has_option(user, 'webhookid'):
# 	WEBHOOK_ID = r.config.CONFIG[user]['webhookid']
# else:
# 	log.error("Webhookid not in config, aborting")
# 	sys.exit(0)
#
# if r.config.CONFIG.has_option(user, 'tokenid'):
# 	TOKEN_ID = r.config.CONFIG[user]['tokenid']
# else:
# 	log.error("Tokenid not in config, aborting")
# 	sys.exit(0)
#
# WEBHOOK = WEBHOOK.format(WEBHOOK_ID, TOKEN_ID)
# requests.post(WEBHOOK, data={"content": count_string})

# reddit = StartingTheBot(Botname)
# subreddit = reddit.subreddit(OurSubreddit)
#
# def PullandUnzipUsernotes(authorizeduser,chosenwarning):
#     allusernotes = json.loads(subreddit.wiki['usernotes'].content_md) # Extracts the whole usernotes page and turns it into a dictionary.
#     blob = base64.b64decode(allusernotes['blob']) # Focuses our attention on the blob in the usernotes and converts the base64 number into a binary (base2) number.
#     blob = zlib.decompress(blob).decode() # Converts that binary number into a string.
#     blob = json.loads(blob) # Converts that string into a dictionary.
#     moderatorlisted = False
#     for usernumber, user in enumerate(allusernotes['constants']['users']):
#         if user == authorizeduser:
#             moderatornumber = usernumber
#             moderatorlisted = True
#             break
#     if moderatorlisted == False:
#         print("This user is not authorized.")
#     chosenwarningpresent = False
#     for warningnumber, warning in enumerate(allusernotes['constants']['warnings']):
#         if warning == chosenwarning:
#             chosenwarningnumber = warningnumber
#             chosenwarningpresent = True
#             break
#     if chosenwarningpresent == False:
#         print("This option is not available.")
#     return [allusernotes, blob, moderatornumber, chosenwarningnumber]
#
# def MakeNewNote(blob, note, moderatornumber, chosenwarningnumber, parent):
#     # print(blob,note,moderatornumber,chosenwarningnumber,parent)
#     newnote = {
#     'n':note, # The displayed note.
#     't':int(time.time()), # The time the note is made.
#     'm':moderatornumber, # The moderator number that made the note.
#     'l':parent.fullname, # The attached link.
#     'w':chosenwarningnumber # The warning number.
#     }
#     try:
#         print("This user has been noted before.")
#         print(blob[parent.author.name]['ns'])
#         blob[parent.author.name]['ns'] = [newnote] + blob[parent.author.name]['ns']
#     except:
#         blob[parent.author.name] = {'ns':list()}
#         blob[parent.author.name]['ns'] = [newnote]
#     print(blob[parent.author.name]['ns'])
#     return blob
#
# def CompileandZipUsernotes(allusernotes, blob, moderator):
#     # This is the debugging code. Disable or delete this when you're done debugging.
#     # print(allusernotes)
#     # print(blob)
#
#     blob = json.dumps(blob)
#     blob = blob.encode()
#     blob = zlib.compress(blob)
#     rewrittenblob = base64.b64encode(blob).decode()
#     allusernotes['blob'] = str(rewrittenblob)
#     allusernotes = json.dumps(allusernotes)
#     subreddit.wiki['usernotes'].edit(allusernotes,reason="your reason for " + moderator)

# PUBLIC_ENUMS = {
# 	'Action': Action
# }
#
#
# class EnumEncoder(json.JSONEncoder):
# 	def default(self, obj):
# 		for enum in PUBLIC_ENUMS.values():
# 			if type(obj) is enum:
# 				return {"__enum__": str(obj)}
# 		return json.JSONEncoder.default(self, obj)
#
#
# def as_enum(d):
# 	if "__enum__" in d:
# 		name, member = d["__enum__"].split(".")
# 		return getattr(PUBLIC_ENUMS[name], member)
# 	else:
# 		return d
#
#
# def embedTableInMessage(message, table):
# 	if table is None:
# 		return message
# 	else:
# 		return "{}{}{})".format(message, globals.datatag, json.dumps(table, cls=EnumEncoder).replace(" ", "%20"))
#
#
# def extractTableFromMessage(message):
# 	datatagLocation = message.find(globals.datatag)
# 	if datatagLocation == -1:
# 		return None
# 	data = message[datatagLocation + len(globals.datatag):-1].replace("%20", " ")
# 	try:
# 		table = json.loads(data, object_hook=as_enum)
# 		return table
# 	except Exception:
# 		log.debug(traceback.format_exc())
# 		return None


# markdown = [
# 	{'value': "[", 'result': "%5B"},
# 	{'value': "]", 'result': "%5D"},
# 	{'value': "(", 'result': "%28"},
# 	{'value': ")", 'result': "%29"},
# ]
#
#
# def escapeMarkdown(value):
# 	for replacement in markdown:
# 		value = value.replace(replacement['value'], replacement['result'])
# 	return value
#
#
# def unescapeMarkdown(value):
# 	for replacement in markdown:
# 		value = value.replace(replacement['result'], replacement['value'])
# 	return value


# def saveGameObject(game):
# 	file = open("{}/{}".format(globals.SAVE_FOLDER_NAME, game.thread), 'wb')
# 	pickle.dump(game, file)
# 	file.close()
#
#
# def loadGameObject(threadID):
# 	try:
# 		file = open("{}/{}".format(globals.SAVE_FOLDER_NAME, threadID), 'rb')
# 	except FileNotFoundError as err:
# 		log.warning("Game file doesn't exist: {}".format(threadID))
# 		return None
# 	game = pickle.load(file)
# 	file.close()
# 	return game


# def renderDatetime(dtTm, includeLink=True):
# 	localized = pytz.utc.localize(dtTm).astimezone(globals.EASTERN)
# 	timeString = localized.strftime("%m/%d %I:%M %p EST")
# 	if not includeLink:
# 		return timeString
# 	base = "https://www.timeanddate.com/countdown/afootball?p0=0&msg=Playclock&iso="
# 	return "[{}]({}{})".format(timeString, base, dtTm.strftime("%Y%m%dT%H%M%S"))

# datetime.utcfromtimestamp(submission.created_utc + 1)


