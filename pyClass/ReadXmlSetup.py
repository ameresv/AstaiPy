import xml.etree.ElementTree as ET
import pathlib

# Path class Directori
pathFile = str(pathlib.Path(__file__).parent.absolute())
NameSetup = '\\SaveSetup.xml'


def readxml():
    fileswork = []
    tree = ET.parse(pathFile+NameSetup)
    root = tree.getroot()
    tag = root.tag
    attr = root.attrib
    for f in root.findall('File'):
        fileswork.append(f.text)
        return fileswork
