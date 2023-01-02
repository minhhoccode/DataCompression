import heapq
from heapq import heappop
from heapq import heappush
from random import random
from functools import total_ordering
from Utils import *
from time import time


@total_ordering
class Node(object):
    def __init__(self, key=None, weight=None):
        self._key = key
        self._weight = weight
        self._random = random()
        self._children = []

    def addChild(self, obj):
        self._children.append(obj)

    def __eq__(self, other):
        return (self._weight, self._random) == (other._weight, other._random)

    def __lt__(self, other):
        return (self._weight, self._random) < (other._weight, other._random)

def huffmanEncode(Freq):
    data = [Node(x[0], x[1]) for x in Freq]
    heapq.heapify(data)
    while len(data) >= 2:
        child1 = heappop(data)
        child2 = heappop(data) 
        parent = Node(None, child1._weight + child2._weight)
        parent.addChild(child1)
        parent.addChild(child2)
        heappush(data, parent)
    return data

def traverseTree(root, Code, keyCode):
    if len(root._children) == 0:
        keyCode[root._key] = Code
        return
    traverseTree(root._children[0], Code+'0', keyCode)
    traverseTree(root._children[1], Code+'1', keyCode)

def get_code(root):
    Code = ""
    keyCode = dict()
    traverseTree(root[0], Code, keyCode)
    return keyCode

if __name__ == '__main__':
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
    start = time()
    code = get_code(huffmanEncode(freq.items()))
    encoded  = encoded_text (text,code)
    end = time() - start
    print('Thời gian mã hóa là:', end)
    start = time()
    decoded = decoded_text(code, encoded)
    end = time() - start
    print('Thời gian giải mã là:', end)
    display_(text, encoded, decoded, code)