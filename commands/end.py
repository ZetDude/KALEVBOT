def run(message, prefix, alias):
    newdeadline = "END"
    deadline = "The relay has ended. I hope everyone had fun!"
    f = open("C:/Users/Administrator/Desktop/KALEVBOT/deadline.txt", "w")
    f.write(str(newdeadline))
    return "m", [message.channel, deadline]

def help_use():
    return "Mark the relay as ended"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "end"

def help_perms():
    return 4

def help_list():
    return "Mark the relay as ended"

def alias():
    return ['end', 'endrelay']