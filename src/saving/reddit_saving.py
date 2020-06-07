# if you need to track whether you have processed a specific comment or post, the simplest way to do it is to save it
# this does have a slight performance impact since saving the submission is another reddit api call, but unless you
# have a really active bot, it's unlikely to make a noticeable difference
import praw
r = praw.Reddit("BotAccount")
for submission in r.subreddit("ExampleSubreddit"):
	# if the submission is not saved
	if not submission.saved:
		# do something
		# then save it
		submission.save()


# the next approach is to save to a wiki page.
# if the wiki page is a comma separated list of ids, fetch the page
wiki_page = r.subreddit("ExampleSubreddit").wiki["bot_config"]
# split the content by commas into a list
ids = wiki_page.content_md.split(",")
for id in ids:
	print(id)
# add a new ID at the end
ids.append("12345")
# join the list of ids together into a new string and edit the wiki page with it
wiki_page.edit(','.join(ids))


# I have one bot that sends out messages to people, then needs to know what they are replying to when they reply.
# Rather than keeping track of the messages locally, I embed a bit of data in the message itself. Then when I get
# a reply, I check the parent message and pull out the embedded data. The data is stored in empty link markdown, so
# it is effectively invisible to the end user

# I use enums in my code to describe some states, which the default json encoder doesn't like. So here's a bit of
# code I use to translate the enums to and from strings
import json
from enum import Enum


class Action(Enum):
	THING = 1
	OTHER = 2


PUBLIC_ENUMS = {
	'Action': Action
}
datatag = " [](#datatag"


class EnumEncoder(json.JSONEncoder):
	def default(self, obj):
		for enum in PUBLIC_ENUMS.values():
			if type(obj) is enum:
				return {"__enum__": str(obj)}
		return json.JSONEncoder.default(self, obj)


def as_enum(d):
	if "__enum__" in d:
		name, member = d["__enum__"].split(".")
		return getattr(PUBLIC_ENUMS[name], member)
	else:
		return d


def embed_table_in_message(message, table):
	if table is None:
		return message
	else:
		return "{}{}{})".format(message, datatag, json.dumps(table, cls=EnumEncoder).replace(" ", "%20"))


def extract_table_from_message(message):
	datatagLocation = message.find(datatag)
	if datatagLocation == -1:
		return None
	data = message[datatagLocation + len(datatag):-1].replace("%20", " ")
	try:
		table = json.loads(data, object_hook=as_enum)
		return table
	except Exception:
		print("Error extracting message")
		return None


# then it is used like this
message = "Hey! Something happened! Reply to this message with your next action"
data_to_embed = {'action': Action.THING, 'thread': "12345"}
embeded_message = embed_table_in_message(message, data_to_embed)
r.redditor("User").message("subject", message)

incoming_message = next(r.inbox.unread())
extracted_data = extract_table_from_message(incoming_message.body)
