import requests
from bs4 import BeautifulSoup

<<<<<<< HEAD
help_info = {"use": "Conjugate an Estonian verb in many distinct forms, some are left out as they"+
                    " are easily derived from other forms",
             "param": "{}conjugate <*WORD>\n<*WORD>: Word to conjugate",
             "perms": None,
             "list": "Conjugate Estonian verbs"}
alias_list = ['conjugate', 'pööra']

@asyncio.coroutine
def run(message, prefix, alias_name):
    cmdlen = len(prefix + alias_name)
    opstring = message.content[cmdlen:].strip()
    word = opstring
    url = "http://www.filosoft.ee/gene_et/gene.cgi"

    fetch_conjugations = [" n, ", " d, ", " b, ", " me, ", " te, ", " vad, ", " takse, ", " sin, ",
                          " s, ", " ti, ", " o, ", " ge, ", " ks, ", " vat, ", " tavat, ", " nud, "
                         ]
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
=======
page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
print(page.status_code)
>>>>>>> f36a8c3e6790ce39d4c12307dfc6edaa9a4bc5ae
