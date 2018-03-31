import os
import sys
import maincore as core
import sqlite3 as lite

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

help_info = {"use": "Give someone a hug!",
             "param": "{}hug [**MENTIONS]\n[**MENTIONS]: Any amount of mentions of users to hug",
             "perms": None,
             "list": "Give someone a hug!"}
alias_list = ['hug']

def run(message, prefix, aliasName):
    cmdlen = len(prefix + aliasName)
    opstring  = message.content[cmdlen:].strip()
    if opstring == "" or [message.author] == message.mentions:
        combine = "Who are you going to hug, {}? Yourself?".format(message.author.mention)
    else:
        con = lite.connect(sp + "/important/userdata.db")
        if opstring == "--top":
            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Hug ORDER BY Hugs DESC LIMIT 5")
                rows = cur.fetchall()
                combine = "```\nTOP HUGGERS:\n---------\n"
                for row in rows:
                    target_user = core.cl.get_user(row[0])
                    combine += target_user.name if not None else row[0]
                    combine += " - " + str(row[1]) + "\n"
                combine += "\n```"
        else:
            if message.author in message.mentions:
                message.mentions.remove(message.author)
            with con:
                cur = con.cursor()
                cur.execute("SELECT COALESCE(Hugs, 0) FROM Hug WHERE id = ?", (message.author.id,))
                row = cur.fetchone()
                hugs = 0 if row is None else row[0]
                hugs += len(message.mentions)
                cur.execute("INSERT OR IGNORE INTO Hug VALUES(?, ?)", (message.author.id, hugs))
                cur.execute("UPDATE Hug SET Hugs=? WHERE id=?", (hugs, message.author.id))

            if core.cl.user.id in [x.id for x in message.mentions]:
                combine = "Kalev hugs you back, {}! (You've given {} hug(s) in total)".format(message.author.mention, hugs)
            elif len(message.mentions) > 0:
                recievers = " and ".join([x.name for x in message.mentions])
                combine = "{} gave {} a hug! (You've given {} hug(s) in total)".format(message.author.mention, recievers, hugs)
            else:
                recievers = opstring
                combine = "{} gave {} a hug! (You've given {} hug(s) in total)".format(message.author.mention, recievers, hugs)
    core.send(message.channel, combine)

