import math
def get_freq(text):
    freq = dict()
    for c in text:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1
    freq = dict(sorted([(a,freq[a]) for a in freq if freq[a]>0.0], key = lambda el: el[1], reverse = True))
    Nin = sum([freq[a] for a in freq])
    freq = dict([(a,freq[a]/Nin) for a in freq])
    return freq
def encoded_text( text,code):
    encoded = ''
    for char in text:
        encoded += code[char]
    return encoded
def decoded_text(code, encoded):
    decoded = ''
    temp = ''
    for bit in encoded:
        temp += bit
        for char in code:
            if code[char] == temp:
                decoded += char
                temp = ''
    return decoded

def write_to_file(filename, text):
    f = open(filename, 'w+')
    f.write(text)
    f.close()
def read_from_file(filename):
    f = open(filename, 'r')
    text = f.read()
    f.close()
    return text
def compress_percent(text, encoded, decoded, code = ''):
    if text == decoded:
        print ('Giải mã đúng')
    else:
        print ('Giải mã không giống xâu ban đầu')
    if type(encoded) == list:
        encoded = ''.join(str(i) for i in encoded)
    result = round((1 - (len(encoded)/8 + len(str(code)))/len(text))*100, 9)
    if result < 0:
        print ('Độ dài xâu mã hoá và mã nhị phân cho từng kí tự gửi đi cho ra xâu lớn hơn xâu ban đầu')
        print(len(encoded), len(str(code)), len(text))
        return round(((len(encoded)/8 + len(str(code)))/len(text))*100, 9)
    return result

def display_(text, encoded, decoded, code = None):
    choice2 = int(input('Bạn có muốn lưu file mã hoá không?\n1. Có\n2. In ra màn hình là được\n'))

    if choice2 == 1:
        choice2 == True
        file = input('Nhập đường dẫn file lưu: ')
    else:
        print("Lưu ý: Việc viết ra màn hình có thể sẽ không biểu thị hết toàn bộ kí tự\nNên nếu bạn muốn xem hết toàn bộ xâu, hãy chọn lưu file mã hoá\n")
        file = None
    print("Mã hoá:\t", end='')
    if file==None:
        print(encoded)
    else:
        write_to_file(file, encoded)

    choice3 = int(input('Bạn có muốn lưu file giải mã không?\n1. Có\n2. In ra màn hình là được\n'))

    if choice3 == 1:
        write_to_file(input('Nhập đường dẫn file lưu: '), decoded)
    else:
        print("Lưu ý: Việc viết ra màn hình có thể sẽ không biểu thị hết toàn bộ kí tự\nNên nếu bạn muốn xem hết toàn bộ xâu, hãy chọn lưu file mã hoá\n")
        print('Giải mã:\t' + decoded)
    print("%Compress =\t"+str(compress_percent(text, encoded, decoded, code)))
