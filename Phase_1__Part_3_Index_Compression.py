import json
import os


def number_to_gamma_code(number):
    if number == 0:
        return ''

    offset = bin(number)[3:]
    length = '1' * len(offset) + '0'

    return length + offset


def gamma_code_to_number(gamma_code):
    length = len(gamma_code)
    offset = gamma_code[length // 2 + 1:]
    binary = '0b1' + offset

    return int(binary, 2)


def encode_gamma_sequence(nums):
    result = ''
    for num in nums:
        result += number_to_gamma_code(num)

    return result


def decode_gamma_sequence(seq):
    result = []

    start_pos, index, length = 0, 0, 0
    while start_pos < len(seq):
        if seq[index] == '0':
            num = gamma_code_to_number(seq[start_pos: start_pos + 2 * length + 1])
            result.append(num)

            # New Values
            start_pos += 2 * length + 1
            index, length = start_pos, 0

        else:
            length += 1
            index += 1

    return result


def number_to_vb(number):
    result = ''

    binary = bin(number)[2:]
    first_bit = '1'
    while len(binary) > 7:
        byte = first_bit + binary[-7:]
        result += byte[::-1]
        binary = binary[:-7]

        if first_bit == '1':
            first_bit = '0'

    if len(binary) > 0:
        byte = first_bit + '0' * (7 - len(binary)) + binary
        result += byte[::-1]

    return result[::-1]


def vb_to_number(vb_code):
    binary = ''
    num_of_bytes = len(vb_code) // 8

    for i in range(num_of_bytes):
        binary += vb_code[8 * i + 1:8 * (i + 1)]
    binary = '0b' + binary

    return int(binary, 2)


def encode_vb_sequence(nums):
    result = ''
    for num in nums:
        result += number_to_vb(num)

    return result


def decode_vb_sequence(seq):
    result = []
    num_of_bytes = len(seq) // 8

    start_byte = 0
    for i in range(num_of_bytes):
        if seq[8 * i] == '1':
            num = vb_to_number(seq[8 * start_byte: 8 * (i + 1)])
            result.append(num)

            start_byte = i + 1

    return result


def numbers_to_gaps(numbers):
    gaps = [numbers[0]]

    for i in range(1, len(numbers)):
        gaps.append(numbers[i] - numbers[i - 1])

    return gaps


def gaps_to_numbers(gaps):
    numbers = [gaps[0]]

    for i in range(1, len(gaps)):
        numbers.append(numbers[i - 1] + gaps[i])

    return numbers


# For Test

# print(number_to_gamma_code(1025))
# print(gamma_code_to_number('111111111100000000001'))
# print(encode_gamma_sequence([2, 3]))
# print(decode_gamma_sequence('1110001110101011111101101111011'))

# print(number_to_vb(214577))
# print(vb_to_number('0000011010111000'))
# print(decode_vb_sequence('10000101'))
# print(decode_vb_sequence('000001101011100010000101000011010000110010110001'))

# print(numbers_to_gaps([800, 805, 1000]))
# print(gaps_to_numbers([800, 5, 195]))

def encode(trie_dict):
    store_file = open('store_file_compressed', 'wb')
    store_file.write(b'{')
    for word in trie_dict:
        store_file.write(b'"')
        store_file.write(word.encode('utf8'))
        store_file.write(b'":{')

        for doc in trie_dict[word]:
            store_file.write(b'"')
            store_file.write(bytes([int(doc)]))
            store_file.write(b'":[')

            gaps = numbers_to_gaps(trie_dict[word][doc])

            # Gamma Code
            # encoded = '1' + ic.encode_gamma_sequence(gaps)
            # Variable Byte
            encoded = '1' + encode_vb_sequence(gaps)

            bytes_required = int(len(encoded) / 8) + 1
            store_file.write(bytes_required.to_bytes(1, 'big'))
            store_file.write(int(encoded, 2).to_bytes(bytes_required, 'big'))

            store_file.write(b']')
        store_file.write(b'},')
    store_file.write(b'}')
    store_file.close()
    # len_compressed = os.stat('store_file_compressed').st_size
    # print('after compression:', len_compressed)
    store_file.close()


def decode():
    store_file = open('store_file_compressed', 'rb')
    decoded_str = ''
    decoded_str += store_file.read(1).decode('utf8')
    while True:
        # Reading "
        decoded_str += store_file.read(1).decode('utf8')

        # Reading a word
        decoded_char = store_file.read(1).decode('utf8')
        decoded_str += decoded_char
        while decoded_char != '"':
            decoded_char = store_file.read(1).decode('utf8')
            decoded_str += decoded_char
        # End of reading a word

        # Reading :{"
        decoded_str += store_file.read(3).decode('utf8')

        # Reading doc id
        encoded_char = store_file.read(1)
        encoded_seq = encoded_char
        while encoded_char.decode('utf8') != '"':
            encoded_char = store_file.read(1)
            encoded_seq += encoded_char
        decoded_str += str(int.from_bytes(encoded_seq[:-1], 'big'))
        decoded_str += encoded_char.decode('utf8')
        # End of reading doc id

        # Reading :[
        decoded_str += store_file.read(1).decode('utf8')
        store_file.read(1).decode('utf8')

        # Reading position list
        encoded_char = store_file.read(1)
        encoded_seq = b''
        for i in range(int.from_bytes(encoded_char, 'big')):
            encoded_char = store_file.read(1)
            encoded_seq += encoded_char
        decoded_str += '['

        # Gamma Code
        # gaps = ic.decode_gamma_sequence("{0:b}".format(int.from_bytes(encoded_seq, 'big'))[1:])
        # Variable Byte
        gaps = decode_vb_sequence("{0:b}".format(int.from_bytes(encoded_seq, 'big'))[1:])

        for number in gaps_to_numbers(gaps):
            decoded_str += str(number) + ','
        decoded_str = decoded_str[:-1]
        decoded_str += ']'
        encoded_char = store_file.read(1)
        # End of reading position list
        decoded_str += store_file.read(2).decode()
        decoded_char = store_file.read(1).decode()
        if decoded_char == '}':
            decoded_str += decoded_char
            break
        elif decoded_char == '"':
            store_file.seek(store_file.tell() - 1)
        else:
            print('wrong input')
            exit(-666)
    decoded_str = decoded_str[:-2] + decoded_str[-1]
    store_file.close()
    return decoded_str
