import argparse
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import string

ht = None


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


class HashTableChaining:

    def __init__(self):
        self.ARR_LENGTH = 997
        self.table = [None] * self.ARR_LENGTH

    def get_index(self, key: str):
        return hash(key) % self.ARR_LENGTH

    def insert(self, key: str):
        """
        value will always be non-negative.
        :type key: str
        :rtype: void
        """
        index = self.get_index(key)
        if self.table[index] is None:
            self.table[index] = ListNode(key)
        else:
            cur = self.table[index]
            while True:
                if cur.next is None:
                    break
                cur = cur.next
            cur.next = ListNode(key)

    def lookup(self, key: str):
        """
        Returns the value to which the specified key is mapped, or -1 if this map contains no mapping for the key
        :type key: int
        :rtype: int
        """
        index = self.get_index(key)
        cur = self.table[index]
        while cur:
            if cur.val == key:
                return index
            else:
                cur = cur.next
        return -1

    def remove(self, key: str):
        """
        Removes the mapping of the specified value key if this map contains a mapping for the key
        :type key: int
        :rtype: void
        """
        index = self.get_index(key)
        cur = prev = self.table[index]
        if not cur:
            return
        if cur.val == key:
            self.table[index] = cur.next
        else:
            cur = cur.next
            while cur:
                if cur.val == key:
                    prev.next = cur.next
                    break
                else:
                    cur, prev = cur.next, prev.next

    def print_table(self):
        for i in self.table:
            if i:
                print(i.val)


class HashTableAddressing:

    def __init__(self):
        self.ARR_LENGTH = 997
        self.table = [None] * self.ARR_LENGTH

    def get_index(self, key: str):
        return hash(key) % self.ARR_LENGTH

    def insert(self, key: str):
        """
        value will always be non-negative.
        :type key: str
        :rtype: void
        """
        index = self.get_index(key)
        if self.table[index] is None:
            self.table[index] = ListNode(key)
        else:
            cur = self.table[index]
            while True:
                if cur.next is None:
                    break
                cur = cur.next
            cur.next = ListNode(key)

    def lookup(self, key: str):
        """
        Returns the value to which the specified key is mapped, or -1 if this map contains no mapping for the key
        :type key: int
        :rtype: int
        """
        index = self.get_index(key)
        cur = self.table[index]
        while cur:
            if cur.val == key:
                return index
            else:
                cur = cur.next
        return -1

    def remove(self, key: str):
        """
        Removes the mapping of the specified value key if this map contains a mapping for the key
        :type key: int
        :rtype: void
        """
        index = self.get_index(key)
        cur = prev = self.table[index]
        if not cur:
            return
        if cur.val == key:
            self.table[index] = cur.next
        else:
            cur = cur.next
            while cur:
                if cur.val == key:
                    prev.next = cur.next
                    break
                else:
                    cur, prev = cur.next, prev.next


def main():

    # build argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='chaining', action='store_true')
    # parser.add_argument('-c', dest='chaining', nargs='?', default=None)
    parser.add_argument('-o', dest='open_addressing', action='store_true')
    # parser.add_argument('-o', dest='open_addressing', nargs='?', default=None)
    args = parser.parse_args()

    global ht
    if args.chaining:
        ht = HashTableChaining()
    elif args.open_addressing:
        ht = HashTableAddressing()

    str = gen_random_string(8)
    ht.insert(str)
    print(ht.lookup(str))
    ht.print_table()


def graph_test():
    x = np.arange(0, math.pi * 2, 0.05)
    y = np.sin(x)
    plt.plot(x, y)
    plt.xlabel("angle")
    plt.ylabel("sine")
    plt.title('sine wave')
    plt.show()


def gen_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str


if __name__ == '__main__':
    # graph_test()
    # gen_random_string(8)
    main()
