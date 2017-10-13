import importlib.machinery
import os
import sys
import datetime
import random
import math
import pickle

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def run(message, prefix, alias):
    finalMessage = ""
    luckyDataLocal = {"winDay": 99, "winHour": 99}
    luckyDataGlobal = {"winDay": 99, "winHour": 99}
    try:
        with open(sp + "/important/lucky/lucky{}.txt".format(message.guild.id), 'rb') as f:
            luckyDataLocal = pickle.loads(f.read())
    except FileNotFoundError:
        print("local lucky[].txt for this guild didn't exist, creating")

    try:
        with open(sp + "/important/lucky/luckyGLOBAL.txt", 'rb') as f:
            luckyDataGlobal = pickle.loads(f.read())
    except FileNotFoundError:
        print("luckyGLOBAL.txt for this guild didn't exist, creating")
    #finalMessage = "\nDEBUG: global\n{}local\n{}\n".format(luckyDataGlobal, luckyDataLocal)
    nowHour = datetime.datetime.now().hour
    nowDay = datetime.datetime.now().day
    allUsersGlobal = [x for x in core.cl.get_all_members() if not x.bot]
    allUsersLocal = [x for x in list(message.guild.members) if not x.bot]
    if nowDay != luckyDataGlobal["winDay"]:
        luckyUserDayObject = random.sample(allUsersGlobal, 1)
        luckyDataGlobal["day"] = [x.id for x in luckyUserDayObject]
        luckyDataGlobal["claimDay"] = 0
    if nowHour != luckyDataGlobal["winHour"]:
        luckyUserHourObject = random.sample(allUsersGlobal, 1)
        luckyDataGlobal["hour"] = [x.id for x in luckyUserHourObject]
        luckyDataGlobal["claimHour"] = 0

    if nowDay != luckyDataLocal["winDay"]:
        winners = math.ceil(len(allUsersLocal) / 15)
        luckyUserDayObject = random.sample(allUsersLocal, winners)
        luckyDataLocal["daySmall"] = [x.id for x in luckyUserDayObject]
        luckyDataLocal["cDs"] = 0
    if nowHour != luckyDataLocal["winHour"]:
        winners = math.ceil(len(allUsersLocal) / 10)
        luckyUserHourObject = random.sample(allUsersLocal, winners)
        luckyDataLocal["hourSmall"] = [x.id for x in luckyUserHourObject]
        luckyDataLocal["cHs"] = 0

    luckyDataGlobal["winDay"] = nowDay
    luckyDataGlobal["winHour"] = nowHour
    luckyDataLocal["winDay"] = nowDay
    luckyDataLocal["winHour"] = nowHour

    finalMessage += message.author.mention + "\n"
    luckyMessage = ""
    credits = 0

    if message.author.id in luckyDataGlobal["hour"]:
        if luckyDataGlobal.get("claimHour", 0) == 0:
            luckyMessage += "CONGRATULATIONS, YOU ARE THE GLOBAL LUCKY USER OF THIS HOUR\n"
            credits += 3000
            luckyDataGlobal["claimHour"] = 1
        else:
            finalMessage += "(You have already claimed your global hourly prize)\n"
    if message.author.id in luckyDataGlobal["day"]:
        if luckyDataLocal.get("claimDay", 0) == 0:
            luckyMessage += "CONGRATULATIONS, YOU ARE THE GLOBAL LUCKY USER OF THIS DAY\n"
            credits += 80000
            luckyDataLocal["claimDay"] = 1
        else:
            finalMessage += "(You have already claimed your global daily prize)\n"
    if message.author.id in luckyDataLocal["hourSmall"]:
        if luckyDataLocal.get("cHs", 0) == 0:
            luckyMessage += "CONGRATULATIONS, YOU WON THE SMALL HOURLY PRIZE\n"
            credits += 2
            luckyDataLocal["cHs"] = 1
        else:
            finalMessage += "(You have already claimed your small hourly prize)\n"
    if message.author.id in luckyDataLocal["daySmall"]:
        if luckyDataLocal.get("cDs", 0) == 0:
            luckyMessage += "CONGRATULATIONS, YOU WON THE SMALL DAILY PRIZE\n"
            credits += 70
            luckyDataLocal["cDs"] = 1
        else:
            finalMessage += "(You have already claimed your small daily prize)\n"

    if credits != 0:
        luckyMessage += "You earned {} non-existent credits".format(credits)

    if luckyMessage == "":
        luckyMessage = "\n**You didn't win anything**"

    finalMessage += luckyMessage

    with open(sp + "/important/lucky/lucky{}.txt".format(message.guild.id), 'wb') as f:

        pickle.dump(luckyDataLocal, f)
    with open(sp + "/important/lucky/luckyGLOBAL.txt", 'wb') as f:

        pickle.dump(luckyDataGlobal, f)

    #finalMessage += "\nDEBUG: global\n{}local\n{}".format(luckyDataGlobal, luckyDataLocal)
    core.send(message.channel, finalMessage)


def help_use():
    return "Check if you are the winner of some amazing prizes"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "lucky"

def help_perms():
    return 0

def help_list():
    return "Check if you are the winner of some amazing prizes"

def alias():
    return ['lucky']
