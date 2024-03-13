from utils.constants import Constants
from drawio.document import Document
from drawio.page import Page

from xml.etree.ElementTree import tostring
import yaml

if __name__ == '__main__':

    with open('bot.yaml', 'r') as file:
        prime_service = yaml.safe_load(file)

        name_flow = (prime_service[Constants.INBOUND_SHORT_MESSAGE][Constants.NAME])
        states = (prime_service[Constants.INBOUND_SHORT_MESSAGE][Constants.STATES])
        tasks = (prime_service[Constants.INBOUND_SHORT_MESSAGE][Constants.TASKS])

        document = Document(name_flow);
        page1 = Page(states[0][Constants.STATE][Constants.NAME], states[0][Constants.STATE][Constants.REFID])
        document.add_page(page1)

        with open(name_flow + '.drawio', 'w') as f:
            f.write(tostring(document.to_xml()).decode())
