from xml.etree.ElementTree import Element
from .page import Page

class Document:
    def __init__(self, title: str):
        self.version = "0.0.1"
        self.host = "mm-conversational-bots"
        self.title = title
        self.type = "embed"
        self.pages: list[Page] = []

    def add_page(self, page):
            self.pages += [page]

    def to_xml(self) -> Element:
        root = Element('mxfile', attrib={
            'host': self.host,
            "version": self.version,
            "type": self.type,
        })

        for page in self.pages:
            root.append(page.to_xml())

        return root