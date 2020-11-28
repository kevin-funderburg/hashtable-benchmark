import argparse
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import string
import time
import sys

NUM_TESTS = 100

"""
the following are constants that are used to determine the size of the hash table
in memory, they were determined by using the sys.getsizeof() call
"""
SIZE_LIST_NODE = 1064       # size of ListNode class
SIZE_EMPTY_HASH_TABLE = 48  # size of hash table with no insertions
SIZE_ARR_NONE = 8           # size of an array index with a None value
SIZE_ARR_STR = 8            # size of an array index with a 8 character string


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
        self.TOTAL_INSERTIONS = 0
        self.table = [None] * self.ARR_LENGTH
        self.set_table_with_load_factor(self.LOAD_FACTOR)

    def set_table_with_load_factor(self, lf):
        """
        insert values into the table based on the load factor
        :param lf:
        :return: void
        """
        filled = round(lf * self.ARR_LENGTH)
        for i in range(filled):
            self.table[i] = ListNode(gen_random_string())
            self.TOTAL_INSERTIONS += 1

    def get_index(self, key: str):
        return hash(key) % self.ARR_LENGTH

    def insert(self, key: str):
        """
        insert a string into the table
        :type key: str
        :return: void
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
        self.TOTAL_INSERTIONS += 1

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
        :type key: str
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
        self.TOTAL_INSERTIONS -= 1

    def get_random_val(self):
        """
        returns the value of a random index in the hash table,
        used for searching/deleting a key
        :return: str
        """
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
        :return: int
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
        self.MEM_SIZE = 48
        self.TOTAL_INSERTIONS = 0
        self.table = [None] * self.ARR_LENGTH
        self.set_table_with_load_factor(self.LOAD_FACTOR)

    def set_table_with_load_factor(self, lf):
        """
        insert values into the table based on the load factor
        :param lf:
        :return: void
        """
        filled = round(lf * self.ARR_LENGTH)
        for i in range(filled):
            self.table[i] = gen_random_string()
            self.TOTAL_INSERTIONS += 1

    def get_index(self, key: str):
        return hash(key) % self.ARR_LENGTH

    def quadratic_probe(self, index, collisions):
        return (index + (collisions ** 2)) % self.ARR_LENGTH

    def insert(self, key: str):
        """
        insert a string into the table
        :type key: str
        :rtype: void
        """
        index = self.lookup(key)
        if index == -1:
            collisions = 0
            index = self.get_index(key)
            while self.table[index] is not None:
                index = self.quadratic_probe(index, collisions)
                collisions += 1
                if collisions == self.ARR_LENGTH:
                    self.double_table()
        self.table[index] = key
        self.TOTAL_INSERTIONS += 1

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
            index = self.quadratic_probe(index, collisions)
            collisions += 1
            if collisions == self.ARR_LENGTH:
                self.double_table()
        return -1

    def remove(self, key: str):
        """
        Removes the mapping of the specified value key if this map contains a mapping for the key
        :type key: int
        :rtype: void
        """
        collisions = 0
        index = hash(key) % self.ARR_LENGTH

        while self.table[index] is not None:
            if self.table[index] == key:
                self.table[index] = None
                return
            index = self.quadratic_probe(index, collisions)
            collisions += 1
            if collisions == self.ARR_LENGTH:
                break
        self.TOTAL_INSERTIONS -= 1

    def get_random_val(self):
        """
        returns the value of a random index in the hash table,
        used for searching/deleting a key
        :return: str
        """
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
    # table_sizes = [100, 1000, 10000]
    table_sizes = [100, 1000, 10000, 100000, 1000000]
    # table_sizes = [100, 1000, 10000, 100000, 1000000, 10000000]
    load_factors = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    if args.chaining:
        for ts in table_sizes:
            for lf in load_factors:
                hash_tables.append(HashTableChaining(ts, lf))
    elif args.open_addressing:
        for ts in table_sizes:
            for lf in load_factors:
                hash_tables.append(HashTableAddressing(ts, lf))

    insertion_test(hash_tables)
    print()
    search_test(hash_tables)
    print()
    deletion_test(hash_tables)
    print()
    mem_test(hash_tables)
    print()
    return


def insertion_test(hash_tables):
    print('{:^60}'.format('INSERTION'))
    table_div()
    print('{:10}'.format('LENGTH') +
          '{:8}'.format('LF') +
          '{:20}'.format('START_INSERTIONS') +
          'TIME')
    table_div()

    for ht in hash_tables:
        start_insertions = ht.TOTAL_INSERTIONS
        insert_times = []
        for i in range(NUM_TESTS):
            rand_string = gen_random_string()
            start_insert_time = time.time()
            ht.insert(rand_string)
            end_insert_time = time.time()
            insert_time = end_insert_time - start_insert_time
            insert_times.append(insert_time)
            ht.remove(rand_string)

        avg_insert_time = avg(insert_times)

        print('{:<10}'.format(ht.ARR_LENGTH) +
              '{:<8}'.format(ht.LOAD_FACTOR) +
              '{:<20}'.format(start_insertions) +
              '{:<20}'.format(avg_insert_time))
    table_div()


def search_test(hash_tables):
    print('{:^60}'.format('SEARCH'))
    table_div()
    print('{:10}'.format('LENGTH') +
          '{:8}'.format('LF') +
          'TIME')
    table_div()

    for ht in hash_tables:
        if ht.LOAD_FACTOR > 0:
            search_times = []
            for i in range(NUM_TESTS):
                search_string = ht.get_random_val()
                start_search_time = time.time()
                ht.lookup(search_string)
                end_search_time = time.time()
                search_times.append(end_search_time - start_search_time)

            avg_search_time = avg(search_times)

            print('{:<10}'.format(ht.ARR_LENGTH) +
                  '{:<8}'.format(ht.LOAD_FACTOR) +
                  '{:<20}'.format(avg_search_time))
    table_div()


def deletion_test(hash_tables):
    print('{:^60}'.format('DELETE'))
    table_div()
    print('{:10}'.format('LENGTH') +
          '{:8}'.format('LF') +
          'TIME')
    table_div()

    for ht in hash_tables:
        if ht.LOAD_FACTOR > 0:
            delete_times = []
            for i in range(NUM_TESTS):
                delete_string = ht.get_random_val()
                start_delete_time = time.time()
                ht.remove(delete_string)
                end_delete_time = time.time()
                delete_times.append(start_delete_time - end_delete_time)

            avg_delete_time = avg(delete_times)

            print('{:<10}'.format(ht.ARR_LENGTH) +
                  '{:<8}'.format(ht.LOAD_FACTOR) +
                  '{:<20}'.format(avg_delete_time))
    table_div()


def mem_test(hash_tables):
    print('{:^60}'.format('MEMORY'))
    table_div()
    print('{:10}'.format('LENGTH') + '{:8}'.format('LF') + '{:17}'.format('MEMORY'))
    table_div()

    for ht in hash_tables:
        print('{:<10}'.format(ht.ARR_LENGTH) +
              '{:<8}'.format(ht.LOAD_FACTOR) +
              '{:<17}'.format(ht.get_mem_size()) +
              '{:<20}'.format(""))
    table_div()


def table_div(): print('{:-^60}'.format(''))


def avg(arr): return sum(arr) / len(arr)


def size_test():
    ht = HashTableAddressing(100, 0.5)
    print("HashTableAddressing(100, 0.5): ", sys.getsizeof(ht))
    ht1 = HashTableAddressing(1000000, 0.5)
    print("HashTableAddressing(1000000, 0.5): ", sys.getsizeof(ht1))
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


def gen_random_string():
    """
    generate a random string of lowercase letters, 8 characters long
    :return:
    """
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(8))
    return result_str


if __name__ == '__main__':
    # graph_test()
    # gen_random_string()
    # size_test()
    main()
