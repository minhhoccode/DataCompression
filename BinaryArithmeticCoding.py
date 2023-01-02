from Utils import *
from time import time
from sys import stdout as so
from math import floor, ceil


def binary_search(a, x, I=0, U=None):
    if I < 0:
        raise ValueError('I không được là số âm')
    if U is None:
        U = len(a)
    while I < U:
        mid = (I+U)//2
        if x < a[mid]:
            U = mid
        else:
            I = mid+1
    return I


def encode(x, p, choice = False):
    precision = 32
    one = int(2**precision - 1)
    quarter = int(ceil(one/4))
    half = 2*quarter
    threequarters = 3*quarter
    p = dict([(a, p[a]) for a in p if p[a] > 0])
    f = [0]
    for a in p:
        f.append(f[-1]+p[a])
    f.pop(-1)
    f = dict([(a, mf) for a, mf in zip(p, f)])
    y = []
    I, U = 0, one
    straddle = 0
    for k in range(len(x)):
        if k % 100 == 0 and choice:
            """
            Mặc dù đã cải thiện tốc độ dựa vào việc thay đổi cách chúng ta làm việc với con số,
            tuy nhiên khi số lượng dữ liệu tăng lên, mã hoá số học vẫn có thể nói là khá chậm. 
            Vì thế em viết thêm 1 số biểu diễn để biết rằng mã hoá đang được chạy tới đâu.
            """
            so.write('Đang mã hoá %d%%    \r' %
                     int(floor(k/len(x)*100)))
            so.flush()
        U_I_Range = U-I + 1
        a = x[k]
        I = I + int(ceil(f[a]*U_I_Range))
        U = I + int(floor(p[a]*U_I_Range))

        if (I == U):
            raise NameError('U - I hội tụ!')
        while True:
            if U < half:
                y.append(0)
                y.extend([1]*straddle)
                straddle = 0
            elif I >= half:
                y.append(1)
                y.extend([0]*straddle)
                straddle = 0
                I -= half
                U -= half
            elif I >= quarter and U < threequarters:
                straddle += 1
                I -= quarter
                U -= quarter
            else:
                break
            I *= 2
            U = U*2 + 1
    straddle += 1
    if I < quarter:
        y.append(0)
        y.extend([1]*straddle)
    else:
        y.append(1)
        y.extend([0]*straddle)
    return(y)


def decode(y, p, n):
    precision = 32
    one = int(2**precision - 1)
    quarter = int(ceil(one/4))
    half = 2*quarter
    threequarters = 3*quarter
    p = dict([(a, p[a]) for a in p if p[a] > 0])
    alphabet = list(p)
    f = [0]
    for a in p:
        f.append(f[-1]+p[a])
    f.pop()
    p = list(p.values())
    y.extend(precision*[0])
    x = n*[0]
    value = int(''.join(str(a) for a in y[0:precision]), 2)
    position = precision
    I, U = 0, one
    for k in range(n):
        if k % 100 == 0:
            so.write('Đang giải mã ... %d%%    \r' % int(floor(k/n*100)))
            so.flush()
        U_I_Range = U - I + 1
        """
        Cải tiến vượt bậc về hiệu năng: phần chậm nhất của decode là tìm ra ký hiệu nào rồi đưa chúng 
        vào một khoảng chứa encoded. Điều này dẫn đến chương trình chạy rất chậm (O(n) với n là kích 
        thước bảng chữ cái) nếu tiến hành bằng cách đơn giản sử dụng loop và so sánh. Ở đây, em sử dụng 
        "binary_search" để giảm thiểu số vòng lặp cần chạy.
        """
        a = binary_search(f, (value-I)/U_I_Range) - 1
        x[k] = alphabet[a]
        I = I + int(ceil(f[a]*U_I_Range))
        U = I + int(floor(p[a]*U_I_Range))
        if (I == U):
            raise NameError('U - I Hội tụ!')
        while True:
            if U < half:
                pass
            elif I >= half:
                I = I - half
                U = U - half
                value = value - half
            elif I >= quarter and U < threequarters:
                I = I - quarter
                U = U - quarter
                value = value - quarter
            else:
                break
            I = 2*I
            U = 2*U + 1
            value = 2*value + y[position]
            position += 1
            if position == len(y):
                raise NameError('Không thể giải mã, có hiện tượng hội tụ!')
    x = ''.join(x)
    return(x)


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
        print(''.join(str(a) for a in encoded))
    else:
        with open(file, 'w+') as f:
            f.write(''.join(str(a) for a in encoded))

    choice3 = int(input('Bạn có muốn lưu file giải mã không?\n1. Có\n2. In ra màn hình là được\n'))

    if choice3 == 1:
        write_to_file(input('Nhập đường dẫn để lưu file: '), decoded)
    else:
        print("Lưu ý: Việc viết ra màn hình có thể sẽ không biểu thị hết toàn bộ kí tự\nNên nếu bạn muốn xem hết toàn bộ xâu, hãy chọn lưu file mã hoá\n")
        print('Giải mã:\t' + decoded)
    print("%Compress =\t"+str(compress_percent(text, encoded, decoded, code)))

if __name__ == '__main__':
    choice = int(input('Chọn (1/2) :\n1. Mã hoá file văn bản\n2. Mã hoá xâu văn bản\n'))
    if choice == 1:
        file = input('Nhập đường dẫn file: ')
        text = read_from_file(file)
    else:
        text = str(input('Nhập xâu cần mã hoá: '))
    p = get_freq(text)
    start = time()
    encoded = encode(text, p)
    end = time() - start
    print('Thời gian mã hoá:\t' + str(end))
    start = time()
    decoded = decode(encoded, p, len(text))
    end = time() - start
    print('Thời gian giải mã:\t', str(end))
    display_(text, encoded, decoded)