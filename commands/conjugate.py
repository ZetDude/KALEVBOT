import importlib.machinery
import os
import sys
import asyncio
import requests
import webbrowser
from bs4 import BeautifulSoup

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

@asyncio.coroutine
def run(message, prefix, aliasName):
    cmdlen = len(prefix + aliasName)
    opstring = message.content[cmdlen:].strip()
    word = opstring
    url = "http://www.filosoft.ee/gene_et/gene.cgi"

    rs = [" n, ", " d, ", " b, ", " me, ", " te, ", " vad, ", " takse, ", " s, ", " ti, ", " o, ", " ge, ", " ks, ", " nuks, ", " vat, ", " tavat, "]
    r = requests.post(url, data = {
        'word': word,
        'gi': rs,
    })

    soup = BeautifulSoup(r.content)
    table = soup.find("table")

    datasets = []
    for row in table.find_all("tr")[:]:
        dataset = [td.get_text().replace('\xa0',' ') for td in row.find_all("td")][0]
        datasets.append(dataset)

    final_message = "\n".join(datasets)
    yield from message.channel.send("```\n" + final_message + "\n```")

def help_use():
    return "Conjugate Estonian verbs"

def help_param():
    return "<WORD*> Word to conjugate"

def help_cmd(prefix):
    return prefix + "conjugate <WORD*>"

def help_perms():
    return 0

def help_list():
    return "Conjugate Estonian verbs"

def aliasName():
    return ['inflect', 'pööra']

