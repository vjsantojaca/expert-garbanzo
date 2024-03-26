from xml.etree.ElementTree import Element as XmlElement, SubElement

from .element import Element

class Diamond(Element):
    def __init__(self, x: int, y: int, width: int, height: int, border_width: int = 1,
                 content: str = "", text_align: str = "center", text_valign: str = "middle", font_size: int=10):
        super().__init__()
        self.border_width = border_width
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.content: str = content
        self.text_align: str = text_align
        self.text_valign: str = text_valign
        self.font_size = font_size

    def to_xml(self):
        cell = XmlElement("mxCell", attrib={
            "id": str(self.id),
            "value": self.content,
            "style": f"shape=rhombus;whiteSpace=wrap;html=1;align={self.text_align};verticalAlign={self.text_valign};fontSize={self.font_size};",
            "vertex": str(self.border_width),
            "parent": "1",
        })

        SubElement(cell, "mxGeometry", attrib={
            "x": str(self.x),
            "y": str(self.y),
            "width": str(self.width),
            "height": str(self.height),
            "as": "geometry",
        })

        return cell