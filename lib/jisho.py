import json
import requests


def lookup(query):

    data = json.loads(
            requests.get("http://jisho.org/api/v1/search/words?keyword={}".format(
                query)).text)

    results = {}

    for result in range(len(data["data"])):

        results[result] = {"readings": [], "words": [], "senses": {}}

        for a in range(len(data["data"][result]["japanese"])):

            if (data["data"][result]["japanese"][a]["reading"] not
                    in results[result]["readings"]):
                results[result]["readings"].append(
                    data["data"][result]["japanese"][a]["reading"])

            if (data["data"][result]["japanese"][a]["word"] not
                    in results[result]["words"]):
                results[result]["words"].append(
                    data["data"][result]["japanese"][a]["word"])

        for b in range(len(data["data"][result]["senses"])):
            results[result]["senses"][b] = {"english": [], "parts": []}

            for c in range(len(data["data"][result]["senses"][b]["english_definitions"])):
                results[result]["senses"][b]["english"].append(
                    data["data"][result]["senses"][b]["english_definitions"][c])

            for d in range(len(data["data"][result]["senses"][b]["parts_of_speech"])):
                results[result]["senses"][b]["parts"].append(
                    data["data"][result]["senses"][b]["parts_of_speech"][d])

    return results
