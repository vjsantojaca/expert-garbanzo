from utils.constants import Constants
from drawio.document import Document
from drawio.page import Page

from xml.etree.ElementTree import tostring
import yaml
import json
import os


if __name__ == '__main__':

    with open('bot.yaml', 'r') as file:
        prime_service = yaml.safe_load(file)
    with open('bot.json', 'w') as json_file:
        json.dump(prime_service, json_file)
    
    flow_json = json.load(open('bot.json'))

    name_flow = (flow_json[Constants.INBOUND_SHORT_MESSAGE][Constants.NAME])
    states = (flow_json[Constants.INBOUND_SHORT_MESSAGE][Constants.STATES])
    tasks = (flow_json[Constants.INBOUND_SHORT_MESSAGE][Constants.TASKS])

    document = Document(name_flow);
    for state in states:
        page = Page("State--" + state[Constants.STATE][Constants.NAME], state[Constants.STATE][Constants.REFID])
        document.add_page(page)

    for task in tasks:
        page = Page("Task--" + task[Constants.TASK][Constants.NAME], task[Constants.TASK][Constants.REFID])
        document.add_page(page)

    with open(name_flow + '.drawio', 'w') as f:
        f.write(tostring(document.to_xml()).decode())
        os.remove('bot.json')
