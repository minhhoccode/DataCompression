from Utils import *
from time import time

class Symbol:
    def __init__(self, char, probability):
        self.char = char
        self.probability = probability
        self.code = ""

def get_code_sf(list):
    def get_split_index(list):
        diff_list = []
        sum = 0.0
        for symbol in list:
            sum += symbol.probability
        half = float(sum / 2)
        s = 0.0
        for i in range(0, len(list)):
            s += list[i].probability
            diff = round(abs(half-s),3)
            diff_list.append([diff, i])
        diff_list = sorted(diff_list)
        return diff_list[0][1]

    sep = get_split_index(list) + 1
    first_list = list[0:sep]
    second_list = list[sep:len(list)]
    for symbol in first_list:
        symbol.code += "0"
    if len(first_list) > 1:
        get_code_sf(first_list)
    for symbol in second_list:
        symbol.code += "1"
    if len(second_list) > 1:
        get_code_sf(second_list)
    for element in second_list:
        first_list.append(element)
    return first_list

def shannon_fano(text, p):
    symbols_list = []
    for key in p:
        symbols_list.append(Symbol(key, p[key]))
    measured_symbols = get_code_sf(symbols_list)
    code = {}
    for symbol in measured_symbols:
        code[symbol.char] = symbol.code
    return code

if __name__ == "__main__":
    choice = int(input('Chọn (1/2) :\n1. Mã hoá file văn bản\n2. Mã hoá xâu văn bản\n'))
    if choice == 1:
        file = input('Nhập đường dẫn file: ')
        text = read_from_file(file)
    else:
        text = str(input('Nhập xâu cần mã hoá: '))
    freq = get_freq(text)
    do = int(input("Bạn có muốn nhập xác suất không? (1: Có, 0: Không): "))
    if do == 1:
        for i in freq:
            freq[i] = float(input("Nhập xác suất của ký tự {}: ".format(i)))
    code = shannon_fano(text, freq)
    start = time()
    encoded  = encoded_text (text,code)
    end = time() - start
    print('Thời gian mã hóa là:', end)
    start = time()
    decoded = decoded_text(code, encoded)
    end = time() - start
    print('Thời gian giải mã là:', end)
    display_(text, encoded, decoded, code)