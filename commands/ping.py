import maincore as core

help_info = {"use": "Pong!",
             "param": "{}ping",
             "perms": None,
             "list": "Pong!"}
alias_list = ['ping', 'pong']

def run(message, prefix, alias_name):
    del prefix
    latency = round(core.cl.latency * 1000)
    pong = "Pong!" if alias_name == "ping" else "Ping!"
    core.send(message.channel, "🏓  {} {} ms latency".format(pong, latency))
