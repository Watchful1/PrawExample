# I reuse praw's praw.ini config file. It can be stored in the project folder, but it can also be stored in a central
# place and contain the configs for multiple projects. Then you can reference them by the name of the reddit account.
# there's an overview of praw's setup here
# https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html

# on my windows computer, I store the praw.ini file in the appdata/roaming folder. Then I copied the code that PRAW
# uses to find it regardless of what operating system I'm on.

import configparser
import os


# this function loads and returns the config file
def get_config():
	config = configparser.ConfigParser()
	if 'APPDATA' in os.environ:  # Windows
		os_config_path = os.environ['APPDATA']
	elif 'XDG_CONFIG_HOME' in os.environ:  # Modern Linux
		os_config_path = os.environ['XDG_CONFIG_HOME']
	elif 'HOME' in os.environ:  # Legacy Linux
		os_config_path = os.path.join(os.environ['HOME'], '.config')
	else:
		raise FileNotFoundError("Could not find config")
	os_config_path = os.path.join(os_config_path, 'praw.ini')
	config.read(os_config_path)

	return config


# then this one looks up a variable in the config
def get_config_var(config, section, variable):
	if section not in config:
		raise ValueError(f"Section {section} not in config")

	if variable not in config[section]:
		raise ValueError(f"Variable {variable} not in section {section}")

	return config[section][variable]


# if I have a praw.ini file like this
'''
[RemindMeBot]
client_id = blablabla
client_secret = blablabla
refresh_token = blablabla
user_agent = blablabla
logging_webhook = https://discord.com/api/webhooks/1111111/blablabla
special_variable = foo

[UpdateMeBot]
client_id = blablabla
client_secret = blablabla
refresh_token = blablabla
user_agent = blablabla
logging_webhook = https://discord.com/api/webhooks/1111111/blablabla
special_variable = bar
'''
# then we can get the special_variable like this
config = get_config()
special_variable = get_config_var(config, "RemindMeBot", "special_variable")

# in the logging section, I introduced my DiscordLogging library. Since that library pulls the logging webhook from
# the praw.ini file, it also includes the functions defined above
import discord_logging
config = discord_logging.get_config()
special_variable = discord_logging.get_config_var(config, "RemindMeBot", "special_variable")
