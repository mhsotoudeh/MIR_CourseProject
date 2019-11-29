class PositionalPostingNode:

    def __init__(self, trie_node, doc_id, position, prev=None):
        self.trie_node = trie_node
        self.doc_id = doc_id
        self.positions = [position]
        self.next = None
        if prev is not None:
            prev.next = self

    def add_entry(self, doc_id, position):
        target_node = self
        while target_node.next is not None:

            if target_node.next.doc_id == doc_id:
                target_node.next.positions.append(position)
                return target_node

            target_node = target_node.next

        target_node.next = PositionalPostingNode(self.trie_node, doc_id, position, target_node)
        return target_node

    # For when a document is deleted from dataset
    def remove(self):
        if self.next is not None:
            self.next = self.next.next

            # reached head - word is not any docs
            if self.doc_id is None and self.next is None:
                print('word no longer exists:', self.trie_node.word)
                TrieNode.WORDS.remove(self.trie_node.word)
                Bigrams.remove_word(self.trie_node.word)
                self.trie_node.posting_list = None
                self.trie_node.word = None
                self.trie_node.check_valid()
        else:
            # should never reach here
            print('error - wrong doc node')


class TrieNode:
    DOCS = dict()
    WORDS = list()

    def __init__(self, parent=None):
        self.parent = parent
        self.word = None
        self.children = dict()
        self.posting_list = None

    def add_word(self, word, doc_id, position, char_index=0):
        if char_index == len(word):
            if self.posting_list is None:
                print('initializing word:', word)
                self.posting_list = PositionalPostingNode(self, None, None)

            if doc_id not in TrieNode.DOCS:
                print('new doc')
                TrieNode.DOCS[doc_id] = set()
            TrieNode.DOCS[doc_id].add(self.posting_list.add_entry(doc_id, position))
            if word not in TrieNode.WORDS:
                TrieNode.WORDS.append(word)
                Bigrams.add_word(word)
                self.word = word
            assert self.word == word
            return

        if word[char_index] not in self.children:
            self.children[word[char_index]] = TrieNode((self, word[char_index]))
        self.children[word[char_index]].add_word(word, doc_id, position, char_index + 1)

    def add_words(self, word_list, doc_id):
        for word, pos in word_list:
            self.add_word(word, doc_id, pos)

    def get_postings_list(self, word):
        iter_node = self
        for char in word:
            if char in iter_node.children:
                iter_node = iter_node.children[char]
            else:
                print("word doesn't exist:", word)
                return
        if iter_node.posting_list is not None and iter_node.word == word:
            print("word found:", word)
            return iter_node.posting_list.next
        else:
            # should never reach here
            print("(shouldn't reach here) word doesn't exist:", word)
            return

    def check_valid(self):
        if self.word is None and not len(self.children.keys()):
            if self.parent is not None:
                del self.parent[0].children[self.parent[1]]
                self.parent[0].check_valid()


class Bigrams:
    _bigrams = dict()
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for c_1 in letters:
        _bigrams[c_1] = dict()
        for c_2 in letters:
            _bigrams[c_1][c_2] = set()

    @staticmethod
    def add_word(word):
        for bigram in find_word_bigrams(word):
            Bigrams._bigrams[bigram[0]][bigram[1]].add(word)

    @staticmethod
    def remove_word(word):
        for bigram in find_word_bigrams(word):
            Bigrams._bigrams[bigram[0]][bigram[1]].remove(word)

    @staticmethod
    def get_similar_words(word):
        results = dict()
        for bigram in find_word_bigrams(word):
            for _w in Bigrams._bigrams[bigram[0]][bigram[1]]:
                if _w not in results:
                    results[_w] = 1
                else:
                    results[_w] += 1
        return results


def find_word_position(tokenized_document, index):
    position = 0
    for i in range(index):
        position += len(tokenized_document[i])

    return position


def find_word_bigrams(word):
    bigrams = []
    for i in range(len(word) - 1):
        bigrams.append(word[i:i + 2])

    return bigrams


def find_document_bigrams(tokenized_document):
    document_bigrams = []
    for word in tokenized_document:
        bigrams = find_word_bigrams(word)

        document_bigrams.extend(bigrams)

    return document_bigrams


d = ['i', 'akbar', 'is', 'lazy', 'islam', 'is']
f = ['akbar']
wr = 'module'

trie = TrieNode()
for w in range(len(d)):
    trie.add_word(d[w], 'd', w)
for w in range(len(f)):
    trie.add_word(f[w], 'f', w)

print(trie.children)
print()
print(TrieNode.DOCS)
print(TrieNode.WORDS)
print()
trie.get_postings_list('akbar')
print(trie.get_postings_list('is').positions)
print(find_word_bigrams('akhbar'))
print(find_word_bigrams('akbar'))
print(Bigrams.get_similar_words('islav'))

for doc in TrieNode.DOCS['d']:
    doc.remove()
del TrieNode.DOCS['d']

print()
trie.get_postings_list('i')
print(trie.children['a'].children)
print(TrieNode.DOCS)
print(TrieNode.WORDS)
print(Bigrams.get_similar_words('islav'))
print(Bigrams.get_similar_words('akaber'))