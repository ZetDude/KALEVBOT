import importlib.machinery
loader = importlib.machinery.SourceFileLoader('basic', 'C:/Users/Administrator/Desktop/KALEVBOT/basic.py')
handle = loader.load_module('basic')

def run(message, rpgPrefix, alias):
                cmdlen = len(rpgPrefix + alias)
                opstring = message.content[cmdlen:].strip()
                try:
                                opstring = int(opstring)
                except:
                                return "m", [message.channel, message.author.mention + ", that isnt a number"]
                targetID = message.author.id
                playerlist = handle.get_playerlist()
                targetEntity = playerlist[targetID]
                out = targetEntity.inspect_slot(opstring)
                return "m", [message.channel, message.author.mention + ", \n```diff\n" + str(out) + "\n```"]

def help_use():
                return "Inspect an item"

def help_param():
                return "<INVENTORY SLOT*>: The inventory slot of the item to inspect."

def help_cmd(prefix):
                return prefix + "inspect <INVENTORY SLOT*>"

def help_perms():
                return 0

def help_list():
                return "Inspect an item."

def alias():
                return ['inspect']
