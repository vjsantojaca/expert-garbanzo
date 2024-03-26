from drawio.diamond import Diamond
from drawio.document import Document
from drawio.line import Line
from drawio.page import Page
from drawio.rectangle import Rectangle
from utils.constants import Constants

from xml.etree.ElementTree import tostring
import yaml
import json
import os

def populate_page_from_actions(actions, page, y_position=0, previous_element=None, first_line_title=None, final_elements=None, first_call=True):
    if final_elements is None:
        final_elements = []

    for action in actions:
        for key, value in action.items():
            if final_elements == []:
                connect_final_elements = False
            else:
                connect_final_elements = True
            if key == Constants.DECISION_TASK or key == Constants.EVALUATEGROUP_TASK:
                content = value[Constants.CONDITION_TASK][Constants.CONDITION_EXP_TASK] if key == Constants.DECISION_TASK else value[Constants.NAME]
                element = Diamond(x=0, y=y_position, width=40, height=40, content=content)

                for key_output, value_output in value[Constants.OUTPUTS_DECISION_TASK].items():
                    final_elements = populate_page_from_actions(value_output[Constants.ACTIONS], page, y_position + 50, element, key_output, final_elements, False)

            elif key == Constants.TRANSFERTOACD_TASK or key == Constants.CALL_TASK:
                element = Rectangle(x=0, y=y_position, width=40, height=40, content=value[Constants.NAME], rounded=True)
            else :
                element = Rectangle(x=0, y=y_position, width=40, height=40, content=value[Constants.NAME])

            if previous_element is not None:
                if first_line_title is None:
                    line = Line(previous_element, element)
                else :
                    line = Line(previous_element, element, content=first_line_title)
                    first_line_title = None
                page.add_content(line)
            
            if (first_call == True and connect_final_elements == True):
                for final_element in final_elements:
                    line = Line(final_element, element)
                    page.add_content(line)
                final_elements = []
            
            if (first_call == False and key != Constants.DECISION_TASK and key != Constants.EVALUATEGROUP_TASK):
                final_elements.append(element)

            page.add_content(element)

            previous_element = element
            y_position += 50

    return final_elements

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
