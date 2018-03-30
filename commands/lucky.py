import os
import sys
import datetime
import random
import math
import pickle
import maincore as core

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
help_info = {"use": "Check if you are the winner of some amazing prizes",
             "param": "{}lucky",
             "perms": None,
             "list": "Check if you are the winner of some amazing prizes"}
alias_list = ['lucky']

def run(message, prefix, alias_name):
    del prefix
    del alias_name
    final_message = ""
    lucky_data_local = {"winDay": 99, "winHour": 99}
    lucky_data_global = {"winDay": 99, "winHour": 99}
    try:
        with open(sp + "/important/lucky/lucky{}.txt".format(message.guild.id), 'rb') as file:
            lucky_data_local = pickle.loads(file.read())
    except FileNotFoundError:
        print("local lucky[].txt for this guild didn't exist, creating")

    try:
        with open(sp + "/important/lucky/luckyGLOBAL.txt", 'rb') as file:
            lucky_data_global = pickle.loads(file.read())
    except FileNotFoundError:
        print("luckyGLOBAL.txt for this guild didn't exist, creating")
    #final_message = "\nDEBUG: global\n{}local\n{}\n".format(lucky_data_global, lucky_data_local)
    now_hour = datetime.datetime.now().hour
    now_day = datetime.datetime.now().day
    all_users_global = [x for x in core.cl.get_all_members() if not x.bot]
    all_users_local = [x for x in list(message.guild.members) if not x.bot]
    if now_day != lucky_data_global["winDay"]:
        lucky_user_day_object = random.sample(all_users_global, 1)
        lucky_data_global["day"] = [x.id for x in lucky_user_day_object]
        lucky_data_global["claimDay"] = 0
    if now_hour != lucky_data_global["winHour"]:
        lucky_user_hour_object = random.sample(all_users_global, 1)
        lucky_data_global["hour"] = [x.id for x in lucky_user_hour_object]
        lucky_data_global["claimHour"] = 0

    if now_day != lucky_data_local["winDay"]:
        winners = math.ceil(len(all_users_local) / 15)
        lucky_user_day_object = random.sample(all_users_local, winners)
        lucky_data_local["daySmall"] = [x.id for x in lucky_user_day_object]
        lucky_data_local["cDs"] = 0
    if now_hour != lucky_data_local["winHour"]:
        winners = math.ceil(len(all_users_local) / 10)
        lucky_user_hour_object = random.sample(all_users_local, winners)
        lucky_data_local["hourSmall"] = [x.id for x in lucky_user_hour_object]
        lucky_data_local["cHs"] = 0

    lucky_data_global["winDay"] = now_day
    lucky_data_global["winHour"] = now_hour
    lucky_data_local["winDay"] = now_day
    lucky_data_local["winHour"] = now_hour

    final_message += message.author.mention + "\n"
    lucky_message = ""
    won_credits = 0

    if message.author.id in lucky_data_global["hour"]:
        if lucky_data_global.get("claimHour", 0) == 0:
            lucky_message += "CONGRATULATIONS, YOU ARE THE GLOBAL LUCKY USER OF THIS HOUR\n"
            won_credits += 3000
            lucky_data_global["claimHour"] = 1
        else:
            final_message += "(You have already claimed your global hourly prize)\n"
    if message.author.id in lucky_data_global["day"]:
        if lucky_data_local.get("claimDay", 0) == 0:
            lucky_message += "CONGRATULATIONS, YOU ARE THE GLOBAL LUCKY USER OF THIS DAY\n"
            won_credits += 80000
            lucky_data_local["claimDay"] = 1
        else:
            final_message += "(You have already claimed your global daily prize)\n"
    if message.author.id in lucky_data_local["hourSmall"]:
        if lucky_data_local.get("cHs", 0) == 0:
            lucky_message += "CONGRATULATIONS, YOU WON THE SMALL HOURLY PRIZE\n"
            won_credits += 2
            lucky_data_local["cHs"] = 1
        else:
            final_message += "(You have already claimed your small hourly prize)\n"
    if message.author.id in lucky_data_local["daySmall"]:
        if lucky_data_local.get("cDs", 0) == 0:
            lucky_message += "CONGRATULATIONS, YOU WON THE SMALL DAILY PRIZE\n"
            won_credits += 70
            lucky_data_local["cDs"] = 1
        else:
            final_message += "(You have already claimed your small daily prize)\n"

    if won_credits != 0:
        lucky_message += "You earned {} non-existent won_credits".format(won_credits)

    if lucky_message == "":
        lucky_message = "\n**You didn't win anything**"

    final_message += lucky_message

    with open(sp + "/important/lucky/lucky{}.txt".format(message.guild.id), 'wb') as file:

        pickle.dump(lucky_data_local, file)
    with open(sp + "/important/lucky/luckyGLOBAL.txt", 'wb') as file:

        pickle.dump(lucky_data_global, file)

    #final_message += "\nDEBUG: global\n{}local\n{}".format(lucky_data_global, lucky_data_local)
    core.send(message.channel, final_message)
