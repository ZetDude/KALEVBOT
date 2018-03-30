import asyncio
import requests
from bs4 import BeautifulSoup

help_info = {"use": "Inflect Estonian nouns or adjectives in many distinct form, some are left out"+
                    " as they are easily derived from other forms",
             "param": "{}inflect <*WORD>\n<*WORD>: Word to inflect",
             "perms": None,
             "list": "Inflect Estonian nouns or adjectives"}
alias_list = ['inflect', 'kääna']

@asyncio.coroutine
def run(message, prefix, alias_name):
    cmdlen = len(prefix + alias_name)
    opstring = message.content[cmdlen:].strip()
    word = opstring
    url = "http://www.filosoft.ee/gene_et/gene.cgi"

    fetch_conjugations = [" sg n, ", " sg g, ", " sg p, ", " pl n, ", " pl g, ", " pl p, ",
                          " sg ill, adt, "]
    post_request = requests.post(url, data = {
        'word': word,
        'gi': fetch_conjugations,
    })

    soup = BeautifulSoup(post_request.content)
    table = soup.find("table")

    datasets = []
    for row in table.find_all("tr")[:]:
        dataset = [td.get_text().replace('\xa0', ' ') for td in row.find_all("td")][0]
        datasets.append(dataset)

    final_message = "\n".join(datasets)
    yield from message.channel.send("```\n" + final_message + "\n```")
