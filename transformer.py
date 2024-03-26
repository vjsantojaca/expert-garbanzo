from drawio.line import Line
from drawio.rectangle import Rectangle
from utils.constants import Constants
from drawio.diamond import Diamond
from drawio.document import Document
from drawio.page import Page

from xml.etree.ElementTree import tostring
import yaml
import json
import os

def populate_page_from_actions(actions, page):
    previous_element = None
    y_position = 0
    for action in actions:
        for key, value in action.items():
            if key == Constants.DECISION_TASK:
                element = Diamond(x=0, y=y_position, width=40, height=40, content=value[Constants.NAME])
            elif key == Constants.TRANSFERTOACD_TASK or key == Constants.CALL_TASK:
                element = Rectangle(x=0, y=y_position, width=40, height=40, content=value[Constants.NAME], rounded=True)
            else :
                element = Rectangle(x=0, y=y_position, width=40, height=40, content=value[Constants.NAME])

            if previous_element is not None:
                line = Line(previous_element, element)
                page.add_content(line)

            page.add_content(element)

            previous_element = element
            y_position += 50


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
        populate_page_from_actions(state[Constants.STATE][Constants.ACTIONS], page)
        document.add_page(page)

    for task in tasks:
        page = Page("Task--" + task[Constants.TASK][Constants.NAME], task[Constants.TASK][Constants.REFID])
        populate_page_from_actions(task[Constants.TASK][Constants.ACTIONS], page)
        document.add_page(page)

    with open(name_flow + '.drawio', 'w') as f:
        f.write(tostring(document.to_xml()).decode())
        os.remove('bot.json')
