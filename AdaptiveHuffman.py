from Utils import *
from time import time
class Node(object):
    def __init__(self, parent=None, left=None, right=None, weight=0, symbol=''):
        super(Node, self).__init__()
        self._parent = parent
        self._left = left
        self._right = right
        self._weight = weight
        self._symbol = symbol
    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, parent):
        self._parent = parent
    @property
    def left(self):
        return self._left
    @left.setter
    def left(self, left):
        self._left = left
    @property
    def right(self):
        return self._right
    @right.setter
    def right(self, right):
        self._right = right
    @property
    def weight(self):
        return self._weight
    @weight.setter
    def weight(self, weight):
        self._weight = weight
    @property
    def symbol(self):
        return self._symbol
    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol

class AdaptiveHuffman(object):
    def __init__(self):
        super(AdaptiveHuffman, self).__init__()
        self.e0 = Node(symbol="e0")
        self.root = self.e0
        self.nodes = []
        self.seen = [None] * 256

    def get_code(self, s, node, code=''):
        if node.left is None and node.right is None:
            return code if node.symbol == s else ''
        else:
            temp = ''
            if node.left is not None:
                temp = self.get_code(s, node.left, code+'0')
            if not temp and node.right is not None:
                temp = self.get_code(s, node.right, code+'1')
            return temp

    def find_largest_node(self, weight):
        for n in reversed(self.nodes):
            if n.weight == weight:
                return n

    def swap_node(self, n1, n2):
        i1, i2 = self.nodes.index(n1), self.nodes.index(n2)
        self.nodes[i1], self.nodes[i2] = self.nodes[i2], self.nodes[i1]
        tmp_parent = n1.parent
        n1.parent = n2.parent
        n2.parent = tmp_parent
        if n1.parent.left is n2:
            n1.parent.left = n1
        else:
            n1.parent.right = n1

        if n2.parent.left is n1:
            n2.parent.left = n2
        else:
            n2.parent.right = n2

    def insert(self, s):
        node = self.seen[ord(s)]
        if node is None:
            spawn = Node(symbol=s, weight=1)
            internal = Node(symbol='', weight=1, parent=self.e0.parent,
                            left=self.e0, right=spawn)
            spawn.parent = internal
            self.e0.parent = internal
            if internal.parent is not None:
                internal.parent.left = internal
            else:
                self.root = internal
            self.nodes.insert(0, internal)
            self.nodes.insert(0, spawn)
            self.seen[ord(s)] = spawn
            node = internal.parent

        while node is not None:
            largest = self.find_largest_node(node.weight)
            if (node is not largest and node is not largest.parent and
                    largest is not node.parent):
                self.swap_node(node, largest)
            node.weight = node.weight + 1
            node = node.parent

    def encode(self, text):
        result = ''
        for s in text:
            if self.seen[ord(s)]:
                result += self.get_code(s, self.root)
            else:
                result += self.get_code('e0', self.root)
                result += bin(ord(s))[2:].zfill(8)
            self.insert(s)
        return result

    def get_ascii(self, bin_str):
        return chr(int(bin_str, 2))

    def decode(self, text):
        result = ''

        symbol = self.get_ascii(text[:8])
        result += symbol
        self.insert(symbol)
        node = self.root

        i = 8
        while i < len(text):
            node = node.left if text[i] == '0' else node.right
            symbol = node.symbol

            if symbol:
                if symbol == 'e0':
                    symbol = self.get_ascii(text[i+1:i+9])
                    i += 8
                result += symbol
                self.insert(symbol)
                node = self.root
            i += 1
        return result
if __name__ == '__main__':
    choice = int(input('Chọn (1/2) :\n1. Mã hoá file văn bản\n2. Mã hoá xâu văn bản\n'))
    if choice == 1:
        file = input('Nhập đường dẫn file: ')
        text = read_from_file(file)
    else:
        text = str(input('Nhập xâu cần mã hoá: '))
    start = time()
    encoded = AdaptiveHuffman().encode(text)
    end = time() - start
    print("Thời gian mã hóa là: ", end)
    start = time()
    decoded = AdaptiveHuffman().decode(encoded)
    end = time() - start
    print("Thời gian giải mã là: ", end)
    display_(text, encoded, decoded)