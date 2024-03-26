import enum
from xml.etree.ElementTree import Element as XmlElement, SubElement
from typing import Union

from .element import Element

class LineStrokeStyle(enum.Enum):
    SOLID = 'solid'
    DASHED = 'dashed'
    DOTTED = 'dotted'

class Line(Element):
    def __init__(self, start: Element, end: Element,
                    stroke_thickness: int = 1, stroke_color: str = "#000000",
                    stroke_style: LineStrokeStyle = LineStrokeStyle.SOLID,
                    rounded: bool = False, curved: bool = False,
                    content: str = "",
                    end_arrow: str = "classic"):
        super().__init__()
        self.start = start
        self.end = end
        self.stroke_thickness = stroke_thickness
        self.stroke_color = stroke_color
        self.stroke_style: LineStrokeStyle = stroke_style
        self.content = content
        self.rounded = rounded
        self.curved = curved
        self.end_arrow = end_arrow

    def to_xml(self):
        cell_style = {
            'html': 1,
            "strokeWidth": self.stroke_thickness,
            "strokeColor": self.stroke_color,
        }
        if self.end_arrow is not None:
            cell_style['end_arrow'] = self.end_arrow
        if self.stroke_style == LineStrokeStyle.DASHED:
            cell_style['dashed'] = 1
        if self.curved:
            cell_style['curved'] = 1
        elif self.rounded:
            cell_style['rounded'] = 1
        else:
            cell_style['rounded'] = 0

        cell_attrib = {
            "id": str(self.id),
            "value": self.content,
            "edge": "1",
            "parent": "1",
            "source": self.start.id,
            "target": self.end.id,
        }

        cell_attrib['style'] = ";".join([f"{key}={val}" for (key, val) in cell_style.items()])

        cell = XmlElement("mxCell", attrib=cell_attrib)

        geometry_attrib = {
            "width": str("50"),
            "height": str("50"),
            "relative": "1",
            "as": "geometry",
        }

        geometry = SubElement(cell, "mxGeometry", attrib=geometry_attrib)

        return cell