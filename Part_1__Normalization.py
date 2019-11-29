import xml.etree.ElementTree as ET
from hazm import *
from nltk import RegexpTokenizer, PorterStemmer
from nltk.corpus import stopwords

english_stop_words = set(stopwords.words('english'))


# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')


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
    pass


language = 'English'

if language == 'English':
    documents = ET.parse('test.xml')
    root = documents.getroot()

    title_index = get_tag_index(root, 'title')
    title = root[title_index].text

    text_index = get_tag_index(root, 'text')
    text = root[text_index].text

    normalized_title = normalize_english(title)
    normalized_text = normalize_english(text)


elif language == 'Persian':
    documents = ET.parse('test.xml')
    root = documents.getroot()

    title_index = get_tag_index(root, 'title')
    title = root[title_index].text

    text_index = get_tag_index(root, 'text')
    text = root[text_index].text

    # Step 1: Normalization and Tokenization
    normalizer = Normalizer()
    normalizer.normalize(title)

    # Step 2: Remove Punctuation

    # Step 3: Remove Stopwords

    # Step 4: Stemming

    pass
