p_all = ["104626896360189952", #ZetDude
         "176793254447022081", #Slorany
         "209276384416235520", #Gufferdk
         "171445355555061760", #Digigon
         "215171991227990017", #Mareck
          ]

p_some = ["97128312651935744",  #Linguist 
          ]

p_black = []


def permission_all():
    return p_all

def permission_some():
    return p_all + p_some

def permission_black():
    return p_black


def shelp(content):
    if content == "countdown":
        return """```
Usage:
k!countdown
Returns the time left in the Relay.
No parameters required
```"""

    if content == "pass":
        return """```
Usage:
k!pass
Returns who has the Relay torch, and who that person has to pass the torch to.
No parameters required
```"""

    if content == "deadline":
        return """```
Usage:
k!deadline
Returns who has the Relay deadline.
No parameters required
```"""

    if content == "time in":
        return """```
Usage:
k!time in <CONTINENT*>/<CITY*>
Returns the time in said place. It's a bit janky.
<CONTINENT*>/<CITY*>: For example: Europe/Tallinn
This is very unstable. Sorry!
```"""

    if content == "help":
        return """```
Usage:
k!help <COMMAND>
Direct Messages this help message, or, shows info about a specific command.
<COMMAND>: Optional. Command to get help about
```"""

    if content == "status":
        return """```
Usage:
k!status
Returns if the bot is working, and for how long.
No parameters required
```"""

    if content == "identify get":
        return """```
Usage:
k!identify <USER> get 
Show the identification text of the user.
<USER>: Optional. The username, ID, or a mention of the target player
Defaults to message sender
```"""

    if content == "identify add":
        return """```
Usage:
k!identify <USER> add <TEXT*>
Add something to a user's identification text
<USER>: Optional. The username, ID, or a mention of the target player
Defaults to message sender
<TEXT*>: The text to add the the target's identification text
```"""

    if content == "google":
        return """```
Usage:
k!google <TEXT*>
Return a link to the google search of the search text.
<TEXT*>: The text to google
```"""

    if content == "urban":
        return """```
Usage:
k!google <TEXT*>
Return a link to the urban dictionary definiton of the text
<TEXT*>: The text to google
```"""

    if content == "night":
        return """```
Usage:
k!night <USER>
Wishes a good night to the target user. Good Night!
<USER>: Optional. The username, ID, or a mention of the target player
Defaults to message sender
```"""

    if content == "wiki":
        return """```
Usage:
k!wiki <LANG*> <TEXT*>
Return the Wikipedia page for the specified term in the specified language
<LANG*>: The language you want to search in
<TEXT*>: The name of the page to get
```"""

    if content == "wikti":
        return """```
Usage:
k!wikti <LANG*> <TEXT*>
Return the Wiktionary page for the specified term in the specified language
<LANG*>: The language you want to search in
<TEXT*>: The name of the page to get
```"""

    if content == "dev":
        return """```
Usage:
k!dev
Try it!
No parameters required
```"""

    if content == "new":
        return """```
Usage:
k!new
Calculate a new Relay deadline, overriding the old one. To be used when the torch is passed
No parameters required
!USERS WITH "ALL" PERMISSION ONLY!
```"""
    if content == "del":
        return """```
Usage:
k!del
Delete the last message the bot sent
No parameters required
!USERS WITH "ALL" PERMISSION ONLY!
```"""

    if content == "chathelp":
        return """```
Usage:
k!chathelp
Post the help in chat. Warning: Fills chat!
No parameters required
!USERS WITH "SOME" PERMISSION ONLY!
```"""

    if content == "say":
        return """```
Usage:
k!say <CHANNEL> <TEXT*>
Say the text specified in the channel specified.
<CHANNEL>: Optional. The channel to send the message in.
Defaults to the channel the k!say command was used in.
<TEXT*>: The text to say.
!USERS WITH "SOME" PERMISSION ONLY!
```"""

    if content == "perms":
        return """```
Usage:
k!perms
Return your permission level.
No parameters required
```"""

    if content == "identify":
        return """'''
Usage:
k!identify <USER> <TYPE*> <STRING>
Add, modify or get the identification notes of people
NOTE!!! THIS COMMAND IS ACTUALLY A COMBINATION OF MULTIPLE COMMANDS
USE THESE TO GET MORE HELP ABOUT THE SPECIFICS:
k!help identify add
k!help identify get
<USER>: Optional. The name+discriminator, ID, or mention of an user.
Defaults to message sender.
<TYPE*>: The type of action to do. The types are:
[add] and [get]
<STRING>: Partially optional. When adding an identification using the add type,
this is the text to add.
```"""
