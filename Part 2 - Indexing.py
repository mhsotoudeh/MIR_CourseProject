class LinkedList:
    def __init__(self):
        self.start = None
        self.length = 0

    def add_node(self, node):
        end = self.start
        while end.next is not None:
            end = end.next

        end.next = node
        self.length += 1


class PositionalPostingNode:
    def __init__(self, doc_id, position):
        self.doc_id = doc_id
        self.position = position
        self.next = None


class NormalPostingNode:
    def __init__(self, doc_id, position):
        self.doc_id = doc_id
        self.next = None


class Trie:
    def __init__(self):
        self.root = None
        self.size = 0

    def add_word(self, word, doc_id):
        pass

    def add_words(self, word_list, doc_id):
        for word in word_list:
            self.add_word(word, doc_id)

    def get_postings_list(self, word):
        pass


class DictionaryNode:
    def __init__(self, char):
        self.char = char
        self.children = []
        self.end_of_word = False

        self.num_of_occurences = 0
        self.posting_list_pointer = None


def find_word_position(tokenized_document, index):
    position = 0
    for i in range(index):
        position += len(tokenized_document[i])

    return position


def find_word_bigrams(word):
    bigrams = []
    for i in range(len(word)-1):
        bigrams.append(word[i:i+2])

    return bigrams


def find_document_bigrams(tokenized_document):
    document_bigrams = []
    for word in tokenized_document:
        bigrams = find_word_bigrams(word)

        document_bigrams.extend(bigrams)

    return document_bigrams

# d = ['akbar', 'is', 'lazy']
# w = 'module'

# print(find_word_position(d, 2))
# print(find_document_bigrams(d))
# print(find_word_bigrams(w))


# Body of the Code
