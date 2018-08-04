"""As the file name says, this needs to be renamed to a file called 'obot.py'.
This file's purpose is to supply the bot with important config and also to store the token securely
"""

BOT_TOKEN = '' # The token of the bot
BOT_PREFIX = ["k!"] # The prefix the bot listens to. Must be a list
BOT_NAME = "KalevBot" # Username of the bot. Updated on runtime
BOT_GAME_NAME = "hello" # The text to be playing. Can be None
BOT_GAME_TYPE = 2 # 0 - Playing, 1 - Streaming, 2 - Listening to, 3 - Watching
OWNER_ID = 104626896360189952 # User ID of the owner

# Locations of files. Can be changed
SHIPFILE = "important/shiplog.pickle"
PECAN_CORPUS = "pecan.txt"
