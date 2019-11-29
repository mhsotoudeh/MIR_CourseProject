def number_to_gamma_code(number):
    if number == 0:
        return ''

    offset = bin(number)[3:]
    length = '1' * len(offset) + '0'

    return length + offset


def gamma_code_to_number(gamma_code):
    length = len(gamma_code)
    offset = gamma_code[length//2+1:]
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
            num = gamma_code_to_number(seq[start_pos : start_pos + 2*length+1])
            result.append(num)

            # New Values
            start_pos += 2*length + 1
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
        binary += vb_code[8*i+1:8*(i+1)]
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
        if seq[8*i] == '1':
            num = vb_to_number(seq[8*start_byte : 8*(i+1)])
            result.append(num)

            start_byte = i + 1

    return result


def numbers_to_gaps(numbers):
    gaps = [numbers[0]]

    for i in range(1, len(numbers)):
        gaps.append(numbers[i] - numbers[i-1])

    return gaps


def gaps_to_numbers(gaps):
    numbers = [gaps[0]]

    for i in range(1, len(gaps)):
        numbers.append(numbers[i-1] + gaps[i])

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
