import xml.etree.ElementTree as ET
from hazm import *
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
from nltk import RegexpTokenizer, PorterStemmer
from nltk.corpus import stopwords
import json
import os

english_stop_words = set(stopwords.words('english'))


def get_tag_index(root, tag):
    for i in range(len(root)):
        if root[i].tag == tag:
            return i


def remove_english_stopwords(tokenized_text):
    return [t for t in tokenized_text if t not in english_stop_words]


def normalize_english(text):
    # Step 1: Tokenization and Remove Punctuation
    tokenizer = RegexpTokenizer('\w+')
    tokenized_text = tokenizer.tokenize(text.lower())

    # Step 2: Remove Stopwords
    tokenized_text = remove_english_stopwords(tokenized_text)

    # Step 3: Stemming
    stemmer = PorterStemmer()
    stemmed_text = [stemmer.stem(t) for t in tokenized_text]

    return stemmed_text


def normalize_persian(text):
    # Step 1: Normalization and Tokenization
    normalizer = Normalizer()
    normalizer.normalize(text)
    tokenized_text = word_tokenize(text)

    # Step 2: Remove Punctuation

    # Step 3: Remove Stopwords

    # Step 4: Stemming

    return tokenized_text


language = 'English'

if language == 'English':
    dir = 'data/00 English/'
    savedir = 'data/01 English/'
    num_of_files = len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])

    for i in range(num_of_files):
        document = ET.parse(dir + str(i) + '.xml')
        root = document.getroot()

        title_index = get_tag_index(root, 'title')
        title = root[title_index].text

        text_index = get_tag_index(root, 'text')
        text = root[text_index].text

        normalized_title = normalize_english(title)
        normalized_text = normalize_english(text)

        output_dict = {}
        output_dict['title'] = normalized_title
        output_dict['text'] = normalized_text

        destination = savedir + str(i) + '.json'
        with open(destination, 'w') as json_file:
            json.dump(output_dict, json_file)


elif language == 'Persian':
    document = ET.parse('testfa.xml')
    root = document.getroot()

    title_index = get_tag_index(root, 'title')
    title = root[title_index].text

    text_index = get_tag_index(root, 'text')
    text = root[text_index].text

    normalized_title = normalize_persian(title)
    normalized_text = normalize_persian(text)

    print(normalized_title)
    print(normalized_text)

    stemmer = Stemmer()
    print(stemmer.stem(text))
