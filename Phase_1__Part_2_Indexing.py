import Phase_1__Part_3_Index_Compression as ic
import json
import os
import shlex


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

    def get_word_repetitions(self):
        return len(self.positions)

    def __repr__(self):
        return 'positions: ' + str(self.positions)


class TrieNode:
    DOCS = dict()
    WORDS = list()

    def __init__(self, parent=None):
        self.parent = parent
        self.word = None
        self.children = dict()
        self.posting_list = None
        self.num_of_docs = None

    def add_word(self, word, doc_id, position, char_index=0):
        if char_index == len(word):
            if self.posting_list is None:
                # print('initializing word:', word)
                self.posting_list = PositionalPostingNode(self, None, None)

            if doc_id not in TrieNode.DOCS:
                # print('new doc')
                TrieNode.DOCS[doc_id] = set()

            TrieNode.DOCS[doc_id].add(self.posting_list.add_entry(doc_id, position))

            if word not in TrieNode.WORDS:
                TrieNode.WORDS.append(word)
                Bigrams.add_word(word)
                self.word = word
                self.num_of_docs = 0
            self.num_of_docs += 1
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
                # print("word doesn't exist:", word)
                return
        if iter_node.posting_list is not None and iter_node.word == word:
            out = dict()
            iter_node = iter_node.posting_list.next
            while iter_node is not None:
                out[iter_node.doc_id] = iter_node.positions
                iter_node = iter_node.next
            return out
        else:
            # should never reach here
            # print(iter_node.posting_list is None)
            # print("(shouldn't reach here) word doesn't exist:", word)
            return

    def get_num_of_docs(self, word):
        iter_node = self
        for char in word:
            if char in iter_node.children:
                iter_node = iter_node.children[char]
            else:
                print("word doesn't exist:", word)
                return
        if iter_node.posting_list is not None and iter_node.word == word:
            return iter_node.num_of_docs
        else:
            # should never reach here
            print("(shouldn't reach here) word doesn't exist:", word)
            return

    def check_valid(self):
        if self.word is None and not len(self.children.keys()):
            if self.parent is not None:
                del self.parent[0].children[self.parent[1]]
                self.parent[0].check_valid()

    def to_dict(self):
        out = dict()
        for word in TrieNode.WORDS:
            out[word] = self.get_postings_list(word)
        return out

    @staticmethod
    def from_dict(inp):
        TrieNode.DOCS = dict()
        TrieNode.WORDS = list()
        TrieNode.DICT_MODE = dict()
        _trie = TrieNode()
        try:
            for word in inp:
                for doc_id in inp[word]:
                    for position in inp[word][doc_id]:
                        _trie.add_word(word, doc_id, position)
        except KeyError:
            print('wrong input format')
        return _trie


class Bigrams:
    _bigrams = dict()
    letters = 'abcdefghijklmnopqrstuvwxyz0123456789ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
    for c_1 in letters:
        _bigrams[c_1] = dict()
        for c_2 in letters:
            _bigrams[c_1][c_2] = []

    @staticmethod
    def add_word(word):
        for bigram in find_word_bigrams(word):
            if word not in Bigrams._bigrams[bigram[0]][bigram[1]]:
                Bigrams._bigrams[bigram[0]][bigram[1]].append(word)

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
        for _w in results:
            results[_w] /= (len(_w) + len(word) - 2 - results[_w])
        return results

    @staticmethod
    def to_dict():
        return Bigrams._bigrams

    @staticmethod
    def from_dict(inp):
        Bigrams._bigrams = inp


# def find_word_position(tokenized_document, index):
#     position = 0
#     for i in range(index):
#         position += len(tokenized_document[i])
#
#     return position


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


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def add_file(trie, dir, id):  # id is filename
    with open(dir + id + '.json', 'r') as f:
        input_dict = json.load(f)
        text = input_dict['text']

        position = 0
        for word in text:
            trie.add_word(word, id, position)
            position += 1


if __name__ == "__main__":
    # Create Trie
    trie = TrieNode()

    # Read each document and add words
    dir = 'data/00 English/'
    while True:
        cmd = input('Enter your command.\n').lower()
        cmd = shlex.split(cmd)

        if cmd[0] == 'exit':
            break

        elif cmd[0] == 'addfile':  # Example: addfile "data/Phase 1 - 01 English/file.json"
            last_slash = cmd[1].rfind('/')
            dir = cmd[1][:last_slash + 1]
            filename = cmd[1][last_slash + 1:-5]
            add_file(trie, dir, filename)

        elif cmd[0] == 'adddir':  # Example: adddir "data/Phase 1 - 01 English"
            dir = cmd[1]
            if dir[-1] != '/':
                dir += '/'
            filenames = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

            for filename in filenames:
                add_file(trie, dir, filename[:-5])

    store_file = open('store_file', 'w', encoding='utf8')
    trie_dict = trie.to_dict()
    json.dump(trie_dict, store_file, ensure_ascii=False)
    store_file.close()

    print(trie.get_postings_list('seek'))
    print('before compression:', os.stat('store_file').st_size)

    # Loading from file
    # store_file = open('store_file', 'r', encoding='utf8')
    # trie_dict = TrieNode.from_dict(json.load(store_file))
    # print(trie_dict.to_dict())
    # store_file.close()

    # Encoding
    # store_file = open('store_file_compressed', 'wb')
    # store_file.write(b'{')
    # for word in trie_dict:
    #     store_file.write(b'"')
    #     store_file.write(word.encode('utf8'))
    #     store_file.write(b'":{')
    #
    #     for doc in trie_dict[word]:
    #         store_file.write(b'"')
    #         store_file.write(bytes([int(doc)]))
    #         store_file.write(b'":[')
    #
    #         gaps = ic.numbers_to_gaps(trie_dict[word][doc])
    #
    #         # Gamma Code
    #         # encoded = '1' + ic.encode_gamma_sequence(gaps)
    #         # Variable Byte
    #         encoded = '1' + ic.encode_vb_sequence(gaps)
    #
    #         bytes_required = int(len(encoded) / 8) + 1
    #         store_file.write(bytes_required.to_bytes(1, 'big'))
    #         store_file.write(int(encoded, 2).to_bytes(bytes_required, 'big'))
    #
    #         store_file.write(b']')
    #     store_file.write(b'},')
    # store_file.write(b'}')
    # store_file.close()

    ic.encode(trie_dict)
    len_compressed = os.stat('store_file_compressed').st_size
    print('after compression:', len_compressed)

    # Decoding
    # store_file = open('store_file_compressed', 'rb')
    # decoded_str = ''
    # decoded_str += store_file.read(1).decode('utf8')
    # while True:
    #     # Reading "
    #     decoded_str += store_file.read(1).decode('utf8')
    #
    #     # Reading a word
    #     decoded_char = store_file.read(1).decode('utf8')
    #     decoded_str += decoded_char
    #     while decoded_char != '"':
    #         decoded_char = store_file.read(1).decode('utf8')
    #         decoded_str += decoded_char
    #     # End of reading a word
    #
    #     # Reading :{"
    #     decoded_str += store_file.read(3).decode('utf8')
    #
    #     # Reading doc id
    #     encoded_char = store_file.read(1)
    #     encoded_seq = encoded_char
    #     while encoded_char.decode('utf8') != '"':
    #         encoded_char = store_file.read(1)
    #         encoded_seq += encoded_char
    #     decoded_str += str(int.from_bytes(encoded_seq[:-1], 'big'))
    #     decoded_str += encoded_char.decode('utf8')
    #     # End of reading doc id
    #
    #     # Reading :[
    #     decoded_str += store_file.read(1).decode('utf8')
    #     store_file.read(1).decode('utf8')
    #
    #     # Reading position list
    #     encoded_char = store_file.read(1)
    #     encoded_seq = b''
    #     for i in range(int.from_bytes(encoded_char, 'big')):
    #         encoded_char = store_file.read(1)
    #         encoded_seq += encoded_char
    #     decoded_str += '['
    #
    #     # Gamma Code
    #     # gaps = ic.decode_gamma_sequence("{0:b}".format(int.from_bytes(encoded_seq, 'big'))[1:])
    #     # Variable Byte
    #     gaps = ic.decode_vb_sequence("{0:b}".format(int.from_bytes(encoded_seq, 'big'))[1:])
    #
    #     for number in ic.gaps_to_numbers(gaps):
    #         decoded_str += str(number) + ','
    #     decoded_str = decoded_str[:-1]
    #     decoded_str += ']'
    #     encoded_char = store_file.read(1)
    #     # End of reading position list
    #     decoded_str += store_file.read(2).decode()
    #     decoded_char = store_file.read(1).decode()
    #     if decoded_char == '}':
    #         decoded_str += decoded_char
    #         break
    #     elif decoded_char == '"':
    #         store_file.seek(store_file.tell() - 1)
    #     else:
    #         print('wrong input')
    #         exit(-666)
    # decoded_str = decoded_str[:-2] + decoded_str[-1]
    # print('decoded:', decoded_str)
    # store_file.close()

    trie_d = TrieNode.from_dict(json.loads(ic.decode()))
    print('checking')
    print(trie_d.get_postings_list('seek'))