import pandas as pd
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element, SubElement

language = 'English'

# Preprocess English Documents
if language == 'English':
    documents = pd.read_csv('data/raw/English.csv')
    for i in range(len(documents.index)):
        title = documents['Title'][i]
        text = documents['Text'][i]

        el = Element('page')
        el_title = SubElement(el, "title")
        el_title.text = title
        el_text = SubElement(el, "text")
        el_text.text = text

        ElementTree(el).write(open('data/English/' + str(i) + '.xml', 'wb'))

# Preprocess Persian Documents
elif language == 'Persian':
    documents = ET.parse('data/raw/Persian.xml')
    root = documents.getroot()

    for i in range(len(root)):
        el = root[i]

        ElementTree(el).write(open('data/Persian/' + str(i) + '.xml', 'wb'), encoding='utf-8')