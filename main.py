import argparse
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import string
import time
import sys

ht = None

SIZE_STR = 49
SIZE_LIST_NODE = 1064


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


class HashTableChaining:

    def __init__(self, length, lf):
        """
        initialize a hash table
        :param length: number of indices in the table
        :param lf: load factor, value between 0 and 1
        """
        self.ARR_LENGTH = length
        self.LOAD_FACTOR = lf
        self.table = [None] * self.ARR_LENGTH
        self.set_table_with_load_factor(self.LOAD_FACTOR)

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

    def set_table_with_load_factor(self, lf):
        filled = round(lf * self.ARR_LENGTH)
        for i in range(filled):
            self.table[i] = ListNode(gen_random_string(8))

    def get_random_val(self):
        found = False
        while not found:
            index = random.choice(self.table)
            if index:
                return index.val

    def print_table(self):
        """
        print the values of the hash table indices
        :return: void
        """
        x = 0
        for i in self.table:
            if i:
                print("[" + str(x) + "]", end='')
                cur = i
                while True:
                    print("-->" + cur.val, end='')
                    cur = cur.next
                    if cur is None:
                        break
                print()
            x += 1


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
    parser.add_argument('-o', dest='open_addressing', action='store_true')
    args = parser.parse_args()

    hash_tables = []
    table_sizes = [100, 1000, 10000, 100000]
    load_factors = [0, 0.25, 0.5, 0.75]
    start_time = time.time()

    if args.chaining:
        for ts in table_sizes:
            for lf in load_factors:
                hash_tables.append(HashTableChaining(ts, lf))
    elif args.open_addressing:
        ht = HashTableAddressing()

    insertion_test(hash_tables)
    search_test(hash_tables)
    return
    # for i in range():
    #     ht.insert(gen_random_string(8))
    # # print(ht.lookup(str))
    # print("--- %s seconds ---" % (time.time() - start_time))
    # ht.print_table()
    # s = sys.getsizeof(HashTableChaining)
    # print('ht size: ' + str(s))
    # ls = sys.getsizeof(ListNode)
    # print('ListNode size: ' + str(ls))
    # print('sizeof 8 str: ' + str(sys.getsizeof('')))


def insertion_test(hash_tables):
    print('{:^70}'.format('INSERTION'))
    table_div()
    print('{:10}'.format('LENGTH') + '{:8}'.format('LF') + '{:17}'.format('NUM_INSERTIONS') + 'TIME')
    table_div()
    for ht in hash_tables:
        start_insert_time = time.time()
        num_insertions = round(ht.ARR_LENGTH*0.5)
        # num_insertions = 1
        for i in range(num_insertions):
            ht.insert(gen_random_string(8))
        end_insert_time = time.time()
        print('{:<10}'.format(ht.ARR_LENGTH) +
              '{:<8}'.format(ht.LOAD_FACTOR) +
              '{:<17}'.format(num_insertions) +
              '{:<20}'.format(end_insert_time - start_insert_time))
    table_div()


def search_test(hash_tables):
    print('{:^70}'.format('SEARCH'))
    table_div()
    print('{:10}'.format('LENGTH') + '{:8}'.format('LF') + '{:17}'.format('SEARCH') + 'TIME')
    table_div()
    for ht in hash_tables:
        search_string = ht.get_random_val()
        start_search_time = time.time()
        ht.lookup(search_string)
        end_search_time = time.time()
        print('{:<10}'.format(ht.ARR_LENGTH) +
              '{:<8}'.format(ht.LOAD_FACTOR) +
              '{:<17}'.format(search_string) +
              '{:<20}'.format(end_search_time - start_search_time))
    table_div()


def table_div():
    print('{:-^70}'.format(''))


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
    return result_str


def get_prime_nums():
    file = open('tablesizes.txt')
    lines = file.readlines()
    for line in lines:
        print(format(line.strip()))


if __name__ == '__main__':
    # graph_test()
    # gen_random_string(8)
    # get_prime_nums()
    main()
