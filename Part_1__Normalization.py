import xml.etree.ElementTree as ET
from hazm import *
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
from nltk import RegexpTokenizer, PorterStemmer
from nltk.corpus import stopwords
import json
import os
import shlex

english_stop_words = set(stopwords.words('english'))
persian_punctuation = '.؟!"{}\[]/()'
persian_stop_words = {'و', 'با', 'از', 'به', 'که', 'آیا'}


def get_tag_index(root, tag):
    for i in range(len(root)):
        if root[i].tag == tag:
            return i


def remove_english_stopwords(tokenized_text):
    return [t for t in tokenized_text if t not in english_stop_words]


def remove_persian_punctuation(tokenized_text):
    return [t for t in tokenized_text if t not in persian_punctuation]


def remove_persian_stopwords(tokenized_text):
    return [t for t in tokenized_text if t not in persian_stop_words]


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
    normalized_text = normalizer.normalize(text)
    tokenized_text = word_tokenize(normalized_text)

    # Step 2: Remove Punctuation and Stopwords
    tokenized_text = remove_persian_punctuation(tokenized_text)
    tokenized_text = remove_persian_stopwords(tokenized_text)

    # Step 4: Stemming and Lemmatizing
    stemmer = Stemmer()
    lemmatizer = Lemmatizer()
    for i in range(len(tokenized_text)):
        stemmed_word = stemmer.stem(tokenized_text[i])
        tokenized_text[i] = lemmatizer.lemmatize(stemmed_word)

    return tokenized_text


def parse_file(language, dir, id):
    document = ET.parse(dir + id + '.xml')
    root = document.getroot()

    title_index = get_tag_index(root, 'title')
    title = root[title_index].text

    text_index = get_tag_index(root, 'text')
    text = root[text_index].text

    if language == 'english':
        normalized_title = normalize_english(title)
        normalized_text = normalize_english(text)

    elif language == 'persian':
        normalized_title = normalize_persian(title)
        normalized_text = normalize_persian(text)

    output_dict = {'title': normalized_title, 'text': normalized_text}
    return output_dict


def parse_file_phase2(dir, id):
    document = ET.parse(dir + id + '.xml')
    root = document.getroot()

    tag_index = get_tag_index(root, 'tag')
    tag = root[tag_index].text

    title_index = get_tag_index(root, 'title')
    title = root[title_index].text

    text_index = get_tag_index(root, 'text')
    text = root[text_index].text

    normalized_title = normalize_english(title)
    normalized_text = normalize_english(text)

    output_dict = {'tag': tag, 'title': normalized_title, 'text': normalized_text}
    return output_dict


if __name__ == "__main__":
    language = input('Enter language.\n').lower()
    while True:
        cmd = input('Enter your command.\n').lower()
        cmd = shlex.split(cmd)

        if cmd[0] == 'exit':
            break

        elif cmd[0] == 'chlang':  # Example: chlang persian
            language = cmd[1]

        elif cmd[0] == 'add':  # Example: add "data/Phase 1 - 00 Persian" "data/Phase 1 - 01 Persian"
            dir, savedir = cmd[1], cmd[2]
            if dir[-1] != '/':
                dir += '/'
            if savedir[-1] != '/':
                savedir += '/'

            filenames = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

            for filename in filenames:
                output_dict = parse_file(language, dir, filename[:-4])
                destination = savedir + filename[:-4] + '.json'
                with open(destination, 'w') as json_file:
                    json.dump(output_dict, json_file)

        elif cmd[0] == 'add_phase2':
            dir, savedir = cmd[1], cmd[2]
            if dir[-1] != '/':
                dir += '/'
            if savedir[-1] != '/':
                savedir += '/'

            filenames = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

            for filename in filenames:
                output_dict = parse_file_phase2(dir, filename[:-4])
                destination = savedir + filename[:-4] + '.json'
                with open(destination, 'w') as json_file:
                    json.dump(output_dict, json_file)