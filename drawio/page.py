from xml.etree.ElementTree import Element, SubElement

class Page:
    def __init__(self, title: str, id:str):
        self.title = title
        self.id = id
        self.content = []
        self.count = 0

    def add_content(self, content):
        content.set_id(self.count + 2)
        self.count += 1
        self.content += [content]

    def to_xml(self):
        page = Element("diagram", attrib={
            "id": self.id,
            "name": self.title,
        })

        graph_model = SubElement(page, "mxGraphModel", attrib={
            "dx": "535",
            "dy": "212",
            "grid": "1",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "page": "1",
            "pageScale": "1",
            "pageWidth": "850",
            "pageHeight": "1100",
            "math": "0",
            "shadow": "0",
        })

        root = SubElement(graph_model, "root")

        SubElement(root, "mxCell", attrib={"id": "0"})
        SubElement(root, "mxCell", attrib={"id": "1", "parent": "0"})

        for content in self.content:
            root.append(content.to_xml())

        return page