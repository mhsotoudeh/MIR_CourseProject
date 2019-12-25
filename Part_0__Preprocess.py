import pandas as pd
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element, SubElement

def get_tag_index(root, tag):
    for i in range(len(root)):
        if root[i].tag == tag:
            return i


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
        document_tree = root[i]
        title_index = get_tag_index(document_tree, 'title')
        revision_index = get_tag_index(document_tree, 'revision')
        text_index = get_tag_index(document_tree[revision_index], 'text')

        el = Element('page')
        el_title = SubElement(el, "title")
        el_title.text = document_tree[title_index].text
        el_text = SubElement(el, "text")
        el_text.text = document_tree[revision_index][text_index].text

        ElementTree(el).write(open('data/Persian/' + str(i) + '.xml', 'wb'), encoding='utf-8')
