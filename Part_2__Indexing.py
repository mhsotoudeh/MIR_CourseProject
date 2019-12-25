from nltk import RegexpTokenizer, PorterStemmer
import Part_3__Index_Comperssion as ic
import json
import os


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
                print("word doesn't exist:", word)
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
            print("(shouldn't reach here) word doesn't exist:", word)
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
    letters = 'abcdefghijklmnopqrstuvwxyzابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
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


# d = ['i', 'اکبر', 'is', 'lazy', 'islam', 'is']
# f = ['اکبر']
# wr = 'module'
#
# trie = TrieNode()
# for w in range(len(d)):
#     trie.add_word(d[w], 'd', w)
# for w in range(len(f)):
#     trie.add_word(f[w], 'f', w)

tokenizer = RegexpTokenizer('\w+')
tokenized_text = tokenizer.tokenize(
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore "
    "magna aliqua. Facilisis sed odio morbi quis. Porttitor lacus luctus accumsan tortor posuere. Sit amet "
    "consectetur adipiscing elit duis tristique sollicitudin. Ullamcorper malesuada proin libero nunc consequat "
    "interdum. Commodo quis imperdiet massa tincidunt nunc pulvinar sapien. Leo duis ut diam quam nulla porttitor. "
    "Sed id semper risus in hendrerit gravida rutrum. Ullamcorper malesuada proin libero nunc. Sit amet cursus sit "
    "amet dictum sit. Fermentum dui faucibus in ornare quam viverra orci sagittis. Non nisi est sit amet facilisis "
    "magna. Mi in nulla posuere sollicitudin aliquam ultrices sagittis orci. Facilisi cras fermentum odio eu feugiat. "
    "Et molestie ac feugiat sed lectus. Adipiscing tristique risus nec feugiat in fermentum posuere urna nec. Vivamus "
    "at augue eget arcu dictum varius duis. Aliquam eleifend mi in nulla posuere sollicitudin aliquam ultrices. "
    "Mollis aliquam ut porttitor leo. Neque gravida in fermentum et sollicitudin. Venenatis lectus magna fringilla "
    "urna. Ac odio tempor orci dapibus ultrices in. Odio ut sem nulla pharetra diam. Massa tincidunt nunc pulvinar "
    "sapien et ligula ullamcorper malesuada proin. Cursus eget nunc scelerisque viverra mauris. Lacinia at quis risus "
    "sed vulputate odio ut. Sit amet aliquam id diam maecenas ultricies mi. Nisl suscipit adipiscing bibendum est "
    "ultricies integer quis. Id donec ultrices tincidunt arcu non sodales. Libero enim sed faucibus turpis in eu mi "
    "bibendum. Odio eu feugiat pretium nibh ipsum. Turpis nunc eget lorem dolor. Vel elit scelerisque mauris "
    "pellentesque pulvinar pellentesque habitant morbi. Semper eget duis at tellus at urna condimentum. Sem fringilla "
    "ut morbi tincidunt augue. Nisl nunc mi ipsum faucibus. Euismod lacinia at quis risus sed. Quis vel eros donec ac "
    "odio tempor orci dapibus ultrices. Phasellus vestibulum lorem sed risus. Augue ut lectus arcu bibendum at. Sit "
    "amet venenatis urna cursus eget nunc scelerisque viverra mauris. Mi ipsum faucibus vitae aliquet nec ullamcorper "
    "sit amet. Accumsan sit amet nulla facilisi morbi tempus iaculis. Sit amet massa vitae tortor. Sit amet purus "
    "gravida quis. Purus sit amet luctus venenatis lectus magna. Turpis tincidunt id aliquet risus feugiat in ante "
    "metus dictum. Viverra orci sagittis eu volutpat odio facilisis mauris sit amet. Hac habitasse platea dictumst "
    "vestibulum rhoncus est. At in tellus integer feugiat scelerisque varius morbi. Odio euismod lacinia at quis. Hac "
    "habitasse platea dictumst vestibulum rhoncus. Feugiat in fermentum posuere urna nec. Augue mauris augue neque "
    "gravida in fermentum. Gravida quis blandit turpis cursus in hac habitasse platea. Convallis posuere morbi leo "
    "urna molestie at elementum eu facilisis. Amet consectetur adipiscing elit pellentesque habitant morbi tristique. "
    "Quam viverra orci sagittis eu volutpat odio facilisis mauris. Vel elit scelerisque mauris pellentesque. Nulla "
    "aliquet porttitor lacus luctus. Tellus mauris a diam maecenas. Duis ultricies lacus sed turpis tincidunt. Nulla "
    "porttitor massa id neque aliquam vestibulum morbi blandit cursus. Sed lectus vestibulum mattis ullamcorper velit "
    "sed. Lectus nulla at volutpat diam ut venenatis tellus in metus. Nulla aliquet porttitor lacus luctus. Risus "
    "nullam eget felis eget nunc lobortis. Donec adipiscing tristique risus nec feugiat in. Aliquam ut porttitor leo "
    "a diam sollicitudin. Ullamcorper a lacus vestibulum sed arcu non odio euismod. Arcu bibendum at varius vel "
    "pharetra. Ullamcorper malesuada proin libero nunc consequat interdum varius sit. Amet luctus venenatis lectus "
    "magna fringilla. Nec nam aliquam sem et tortor consequat id porta nibh. Amet dictum sit amet justo donec enim "
    "diam vulputate ut. Sed viverra ipsum nunc aliquet bibendum. Egestas egestas fringilla phasellus faucibus. Amet "
    "risus nullam eget felis eget nunc lobortis mattis aliquam. Tortor id aliquet lectus proin nibh nisl condimentum. "
    "A diam maecenas sed enim ut sem viverra aliquet. Eleifend donec pretium vulputate sapien nec sagittis aliquam "
    "malesuada bibendum. Nibh mauris cursus mattis molestie a. Est velit egestas dui id ornare. Pretium vulputate "
    "sapien nec sagittis aliquam malesuada bibendum arcu. Consectetur libero id faucibus nisl tincidunt eget nullam "
    "non nisi. Erat velit scelerisque in dictum non consectetur a erat nam. Metus aliquam eleifend mi in nulla "
    "posuere. Est sit amet facilisis magna etiam tempor orci. Ultrices neque ornare aenean euismod elementum nisi "
    "quis eleifend. At varius vel pharetra vel turpis nunc eget lorem dolor. Id consectetur purus ut faucibus "
    "pulvinar elementum integer. In tellus integer feugiat scelerisque varius. Cras pulvinar mattis nunc sed blandit. "
    "Ut sem nulla pharetra diam. Donec enim diam vulputate ut pharetra sit amet aliquam id. In nulla posuere "
    "sollicitudin aliquam ultrices sagittis. Convallis aenean et tortor at risus viverra adipiscing at in. In nulla "
    "posuere sollicitudin aliquam ultrices sagittis. Semper viverra nam libero justo laoreet sit amet cursus sit. Sem "
    "viverra aliquet eget sit amet tellus. Nisl suscipit adipiscing bibendum est ultricies integer quis auctor elit. "
    "Quisque sagittis purus sit amet. Aliquam etiam erat velit scelerisque. Elementum pulvinar etiam non quam lacus. "
    "Malesuada nunc vel risus commodo viverra maecenas. Nunc aliquet bibendum enim facilisis gravida neque convallis "
    "a cras. Ut consequat semper viverra nam libero justo laoreet sit. Vel orci porta non pulvinar neque. Ultrices "
    "dui sapien eget mi proin sed libero. Arcu cursus euismod quis viverra nibh cras pulvinar mattis nunc. "
    "Ullamcorper sit amet risus nullam eget felis eget. Netus et malesuada fames ac turpis egestas sed tempus. Sit "
    "amet porttitor eget dolor morbi non arcu risus quis. Nisl rhoncus mattis rhoncus urna neque viverra justo. Fusce "
    "id velit ut tortor pretium viverra. In iaculis nunc sed augue lacus viverra vitae. Lectus proin nibh nisl "
    "condimentum id venenatis a. Ac turpis egestas integer eget. Nisi est sit amet facilisis magna etiam tempor orci. "
    "Tincidunt ornare massa eget egestas purus. Tellus orci ac auctor augue mauris augue neque gravida in. Amet "
    "porttitor eget dolor morbi non. Posuere sollicitudin aliquam ultrices sagittis. Eget nullam non nisi est. Et "
    "ligula ullamcorper malesuada proin libero. Ullamcorper dignissim cras tincidunt lobortis feugiat vivamus. Lectus "
    "mauris ultrices eros in cursus turpis massa tincidunt. Et ultrices neque ornare aenean euismod. Leo vel orci "
    "porta non pulvinar. Massa sapien faucibus et molestie ac. Et leo duis ut diam quam nulla. Eu facilisis sed odio "
    "morbi. Congue quisque egestas diam in arcu. Est velit egestas dui id ornare arcu odio ut. Ultrices in iaculis "
    "nunc sed augue. Integer vitae justo eget magna fermentum iaculis eu non diam. Egestas pretium aenean pharetra "
    "magna ac. Ut tortor pretium viverra suspendisse potenti nullam. In hac habitasse platea dictumst quisque. "
    "Posuere lorem ipsum dolor sit amet consectetur adipiscing elit duis. Nec sagittis aliquam malesuada bibendum. "
    "Ante metus dictum at tempor. Non pulvinar neque laoreet suspendisse interdum consectetur libero id. Maecenas sed "
    "enim ut sem viverra aliquet eget sit amet. Ut placerat orci nulla pellentesque dignissim enim sit amet. Laoreet "
    "id donec ultrices tincidunt arcu non sodales. Mauris augue neque gravida in fermentum et sollicitudin ac. Nec "
    "feugiat nisl pretium fusce id velit ut tortor. Quis viverra nibh cras pulvinar mattis nunc sed blandit libero. "
    "Vestibulum sed arcu non odio euismod. Eu sem integer vitae justo eget magna fermentum iaculis eu. Viverra "
    "adipiscing at in tellus integer feugiat.".lower())

trie = TrieNode()
for idx in range(len(tokenized_text)):
    trie.add_word(tokenized_text[idx], '101', idx)

store_file = open('store_file', 'w', encoding='utf8')
trie_dict = trie.to_dict()
print(trie_dict)
json.dump(trie_dict, store_file, ensure_ascii=False)
store_file.close()

print(trie.get_postings_list('justo'))
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
print(trie_d.get_postings_list('justo'))
