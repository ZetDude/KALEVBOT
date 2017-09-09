import asyncio

@asyncio.coroutine
def cr_send(message, channel, client):
    print("recieved send instruction at sender.py")
    yield from client.send_message(channel, message)
    
def send(ch, m, cl):    
    cl.loop.create_task(cr_send(m, ch, cl))
    