import math
import struct
from decimal import Decimal, getcontext
from Utils import *
getcontext().prec = 10000


def arithmetic_encode(m, p=None, save_stage=False):
    if p is None:
        p = get_freq(m)
    F = [0]
    for a in p:
        F.append(F[-1]+p[a])
    F.pop(-1)
    F.append(1)
    F.pop(0)
    
    stage = []
    F = [Decimal(i) for i in F]
    I = Decimal(0)
    U = Decimal(1)
    I = I + (U - I) * 0
    U = I + (U - I) * F[0]
    U_prev, I_prev = U, I
    if save_stage:
        stage.append((I, U))
    print ("Stage 1:\nI[1] = ", round(I,5), "\nU[1] = ", round(U,5))
    i = 1
    j = 2
    len_F = len(F)
    print(len_F)
    while (i <= len(m) + 1):
        I = I_prev + (U_prev - I_prev) * F[i % len_F]
        i = i + 1
        U = I_prev + (U_prev - I_prev) * F[i % len_F]
        i = i + 1
        print ("Stage " + str(j) +":\nI["+ str(j) + "] = "+  str(round(I,5))+ "\nU["+ str(j)+ "] = "+ str(round(U,5)))
        j = j + 1
        U_prev, I_prev = U, I
        if save_stage:
            stage.append((I, U))
    return I, U, stage

def nextHigherInteger(a):
    t = math.ceil(a)
    if t == a:
        t += 1
    return t


def shortest(a, b):
    if a == b:
        print("2 Số đưa vào có giá trị bằng nhau")
        print("Kết quả có thể không chính xác, bạn nên cập nhật context.prec để tăng độ chính xác")
        return a
    if a > b:
        swap = a
        a = b
        b = swap
    den = Decimal(1)
    t = nextHigherInteger(a)
    while t >= b:
        a *= 2
        b *= 2
        den *= 2
        t = nextHigherInteger(a)
    return Decimal(t) / den


def float2bin(float_num, num_bits=None):
    float_num = str(float_num)
    if float_num.find(".") == -1:
        integers = float_num
        decimals = ""
    else:
        integers, decimals = float_num.split(".")
    decimals = "0." + decimals
    decimals = Decimal(decimals)
    integers = int(integers)
    result = ""
    num_used_bits = 0
    while True:
        mul = decimals * 2
        int_part = int(mul)
        result = result + str(int_part)
        num_used_bits = num_used_bits + 1
        decimals = mul - int(mul)
        if type(num_bits) is type(None):
            if decimals == 0:
                break
        elif num_used_bits >= num_bits:
            break
    if type(num_bits) is type(None):
        pass
    elif len(result) < num_bits:
        num_remaining_bits = num_bits - len(result)
        result = result + "0"*num_remaining_bits
    integers_bin = bin(integers)[2:]
    result = str(integers_bin) + "." + str(result)
    while result[-1] == "0":
        result = result[:-1]
    return result

text = str(input("Nhập chuỗi cần mã hóa: "))
do = int(input("Bạn có muốn nhập xác suất không? (1: Có, 0: Không): "))
p = get_freq(text)
if do == 1:
    for i in p.keys():
        p[i] = float(input("Xác suất của " + i + ": "))
p = {k: p[k] for k in sorted(p)}
from time import time
start = time()
I, U, stage = arithmetic_encode(text, p)
val = shortest(I, U)
print("Chọn điểm biểu diễn bản tin là  val = ", val)
end = time()
print("Thời gian mã hóa là: ", end - start)
print("Xâu sau mã hoá là = ", float2bin(val))