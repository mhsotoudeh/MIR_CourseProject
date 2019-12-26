import pandas as pd
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element, SubElement
import shlex


def get_tag_index(root, tag):
    for i in range(len(root)):
        if root[i].tag == tag:
            return i


if __name__ == "__main__":
    language = input('Enter language.\n').lower()
    while True:
        cmd = input('Enter your command.\n').lower()
        cmd = shlex.split(cmd)

        if cmd[0] == 'exit':
            break

        elif cmd[0] == 'chlang':
            language = cmd[1]

        elif cmd[0] == 'add':
            dir, savedir = cmd[1], cmd[2]
            if savedir[-1] != '/':
                savedir += '/'

            if language == 'english':
                documents = pd.read_csv(dir)
                for i in range(len(documents.index)):
                    title = documents['Title'][i]
                    text = documents['Text'][i]

                    el = Element('page')
                    el_title = SubElement(el, "title")
                    el_title.text = title
                    el_text = SubElement(el, "text")
                    el_text.text = text

                    ElementTree(el).write(open(savedir + str(i) + '.xml', 'wb'))

            elif language == 'persian':
                documents = ET.parse(dir)
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

                    ElementTree(el).write(open(savedir + str(i) + '.xml', 'wb'), encoding='utf-8')

        elif cmd[0] == 'add_phase2':
            dir, savedir = cmd[1], cmd[2]
            if savedir[-1] != '/':
                savedir += '/'

            documents = pd.read_csv(dir)
            for i in range(len(documents.index)):
                tag = documents['Tag'][i]
                title = documents['Title'][i]
                text = documents['Text'][i]

                el = Element('page')
                el_tag = SubElement(el, "tag")
                el_tag.text = str(tag)
                el_title = SubElement(el, "title")
                el_title.text = title
                el_text = SubElement(el, "text")
                el_text.text = text

                ElementTree(el).write(open(savedir + str(i) + '.xml', 'wb'))