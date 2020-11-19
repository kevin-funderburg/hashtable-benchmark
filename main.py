import argparse
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import string
import time
import sys

# ht = None

SIZE_STR = 49
SIZE_LIST_NODE = 1064
SIZE_EMPTY_HASH_TABLE = 48
SIZE_ARR_NONE = 8
SIZE_ARR_STR = 8


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
        self.MEM_SIZE = SIZE_EMPTY_HASH_TABLE
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
        # self.MEM_SIZE += SIZE_LIST_NODE

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
        options = []
        while True:
            index = random.choice(self.table)
            if index:
                cur = index
                while cur is not None:
                    options.append(cur.val)
                    cur = cur.next
                return random.choice(options)

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

    def get_mem_size(self):
        """
        calculate the total size of the hash table in bytes
        :return: MEM_SIZE
        """
        for index in self.table:
            if index is None:
                self.MEM_SIZE += SIZE_ARR_NONE
            else:
                cur = index
                while cur is not None:
                    self.MEM_SIZE += SIZE_LIST_NODE
                    cur = cur.next
        return self.MEM_SIZE



class HashTableAddressing:

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
        self.MEM_SIZE = 48

    def get_index(self, key: str):
        return hash(key) % self.ARR_LENGTH

    def quadratic_probe(self, key):
        collisions = 0
        stop = False
        slot = hash(key) % self.ARR_LENGTH
        while not stop:
            if self.table[slot] is None:
                # self.table[slot] = string
                stop = True
            else:
                slot = (slot + (collisions ** 2)) % self.ARR_LENGTH
                collisions += 1
            # print('collisions: ', collisions)
        return slot

    def insert(self, key: str):
        """
        value will always be non-negative.
        :type key: str
        :rtype: void
        """
        index = self.lookup(key)
        if index == -1:
            collisions = 0
            index = self.get_index(key)
            while self.table[index] is not None:
                index = (index + (collisions ** 2)) % self.ARR_LENGTH
                collisions += 1
                # print('collisions: ', collisions)
                if collisions == self.ARR_LENGTH:
                    self.double_table()
        self.table[index] = key

    def double_table(self):
        new_length = self.ARR_LENGTH * 2;
        new_table = [None] * new_length
        for i in range(self.ARR_LENGTH):
            new_table[i] = self.table[i]
        self.ARR_LENGTH = new_length
        self.table = new_table

    def lookup(self, key: str):
        """
        Returns the value to which the specified key is mapped, or -1 if this map contains no mapping for the key
        :type key: int
        :rtype: int
        """
        collisions = 0
        index = hash(key) % self.ARR_LENGTH

        while self.table[index] is not None:
            if self.table[index] == key:
                return index
            index = (index + (collisions ** 2)) % self.ARR_LENGTH
            collisions += 1
            # print('collisions: ', collisions)
            if collisions == self.ARR_LENGTH:
                self.double_table()
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
            self.table[i] = gen_random_string(8)

    def get_random_val(self):
        while True:
            index = random.choice(self.table)
            if index:
                return index

    def print_table(self):
        """
        print the values of the hash table indices
        :return: void
        """
        x = 0
        for i in self.table:
            if i:
                print("[" + str(x) + "]: " + i)
            x += 1

    def get_mem_size(self):
        """
        calculate the total size of the hash table in bytes
        :return: MEM_SIZE
        """
        for index in self.table:
            if index is None:
                self.MEM_SIZE += SIZE_ARR_NONE
            else:
                self.MEM_SIZE += SIZE_ARR_STR
        return self.MEM_SIZE

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
        for ts in table_sizes:
            for lf in load_factors:
                hash_tables.append(HashTableAddressing(ts, lf))

    mem_test(hash_tables)
    print()
    return
    insertion_test(hash_tables)
    print()
    search_test(hash_tables)


def insertion_test(hash_tables):
    print('{:^70}'.format('INSERTION'))
    table_div()
    print('{:10}'.format('LENGTH') + '{:8}'.format('LF') + '{:17}'.format('NUM_INSERTIONS') + 'TIME')
    table_div()
    for ht in hash_tables:
        start_insert_time = time.time()
        num_insertions = round(ht.ARR_LENGTH*0.75)
        # num_insertions = 1
        for i in range(num_insertions):
            ht.insert(gen_random_string(8))
        end_insert_time = time.time()
        insert_time = end_insert_time - start_insert_time
        print('{:<10}'.format(ht.ARR_LENGTH) +
              '{:<8}'.format(ht.LOAD_FACTOR) +
              '{:<17}'.format(num_insertions) +
              '{:<20}'.format(insert_time))
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
        search_time = end_search_time - start_search_time
        print('{:<10}'.format(ht.ARR_LENGTH) +
              '{:<8}'.format(ht.LOAD_FACTOR) +
              '{:<17}'.format(search_string) +
              '{:<20}'.format(search_time))
    table_div()


def mem_test(hash_tables):
    print('{:^70}'.format('MEMORY'))
    table_div()
    print('{:10}'.format('LENGTH') + '{:8}'.format('LF') + '{:17}'.format('MEMORY'))
    table_div()
    for ht in hash_tables:
        print('{:<10}'.format(ht.ARR_LENGTH) +
              '{:<8}'.format(ht.LOAD_FACTOR) +
              '{:<17}'.format(ht.get_mem_size()) +
              '{:<20}'.format(""))
    table_div()


def table_div(): print('{:-^70}'.format(''))



def size_test():
    ht = HashTableAddressing(100, 0)
    print("HashTableAddressing(100, 0): ", sys.getsizeof(ht))
    ht1 = HashTableAddressing(100, 0.5)
    print("HashTableAddressing(100, 0.5): ", sys.getsizeof(ht1))
    ht2 = HashTableAddressing(100, 0.75)
    print("HashTableAddressing(100, 0.75): ", sys.getsizeof(ht2))
    ht = HashTableChaining(100, 0)
    print("HashTableChaining(100, 0): ", sys.getsizeof(ht))
    print("ht.MEM_SIZE:", ht.MEM_SIZE)
    ht1 = HashTableChaining(100, 0.5)
    print("ht1.MEM_SIZE:", ht1.MEM_SIZE)
    print("HashTableChaining(100, 0.5): ", sys.getsizeof(ht1))
    ht2 = HashTableChaining(100, 0.75)
    print("HashTableChaining(100, 0.75): ", sys.getsizeof(ht2))
    arr = []
    print("size of arr: ", sys.getsizeof(arr))
    arr = [None]
    print("size of arr: ", sys.getsizeof(arr))
    l = ListNode
    print("size of empty ListNode: ", sys.getsizeof(l))
    l.val = 'andslajd'
    print("size of ListNode with string: ", sys.getsizeof(l))


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


if __name__ == '__main__':
    # graph_test()
    # gen_random_string(8)
    # size_test()
    main()
