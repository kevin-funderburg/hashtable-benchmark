import argparse
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import string
import time
import sys

OUTPUT = 'output.txt'
out = open(OUTPUT, 'w')

NUM_TESTS = 1000
MAX_TABLE_SIZE = 1000000
LOAD_FACTORS = []
TABLE_SIZES = []

"""
the following are constants that are used to determine the size of the hash table
in memory, they were determined by using the sys.getsizeof() call
"""
SIZE_LIST_NODE = 1064       # size of ListNode class
SIZE_EMPTY_HASH_TABLE = 48  # size of hash table with no insertions
SIZE_ARR_NONE = 8           # size of an array index with a None value
SIZE_ARR_STR = 8            # size of an array index with a 8 character string


class GraphData:
    def __init__(self, lf):
        self.lf = lf
        self.sizes = []
        self.avg_times = []
        self.mem_sizes = []
        self.size_time_plots = []


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
        # this line is added to ensure at least one element is inserted if the load
        # factor > 0 but the array is so small that the rounding sets filled to 0
        if lf > 0 and filled == 0:
            filled = 1
        for i in range(filled):
            self.table[i] = ListNode(gen_random_string())
            self.TOTAL_INSERTIONS += 1

    def get_index(self, key: str):
        return hash(key) % self.ARR_LENGTH

    def insert(self, key: str):
        """
        insert a key to the head of the chain at the index
        :type key: str
        :return: void
        """
        index = self.get_index(key)
        if self.table[index] is None:
            self.table[index] = ListNode(key)
        else:
            new_node = ListNode(key)
            cur = self.table[index]
            new_node.next = cur
            self.table[index] = new_node
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

    def is_empty(self):
        for i in self.table:
            if i: return False
        return True


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

    def quadratic_probe(self, key, collisions):
        return (hash(key) + collisions + 3*(collisions**2)) % self.ARR_LENGTH

    def insert(self, key: str):
        """
        insert a string into the table
        :type key: str
        :rtype: void
        """
        index = self.lookup(key)
        if index == -1:
            collisions = 0
            start = index = self.quadratic_probe(key, collisions)
            while self.table[index]:
                collisions += 1
                index = self.quadratic_probe(key, collisions)
                if start == index: break

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
        start = index = self.quadratic_probe(key, collisions)

        while self.table[index]:
            if self.table[index] == key:
                return index
            collisions += 1
            index = self.quadratic_probe(key, collisions)
            if start == index: break

        return -1

    def remove(self, key: str):
        """
        Removes the mapping of the specified value key if this map contains a mapping for the key
        :type key: int
        :rtype: void
        """
        index = self.lookup(key)
        if index != -1:
            self.table[index] = None
            self.TOTAL_INSERTIONS -= 1

    def get_random_val(self):
        """
        returns the value of a random index in the hash table,
        used for searching/deleting a key
        :return: str
        """
        while True:
            index = random.choice(self.table)
            if index: return index

    def print_table(self):
        """
        print the values of the hash table indices
        :return: void
        """
        x = 0
        for i in self.table:
            if i: print("[" + str(x) + "]: " + i)
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

    def is_empty(self):
        for i in self.table:
            if i: return False
        return True


def init():
    """
    initialize constants to be used later
    :return: void
    """
    for lf in np.arange(0.0, 1.0, 0.05):
        LOAD_FACTORS.append(round(lf, 2))

    x = 100
    while x <= MAX_TABLE_SIZE:
        TABLE_SIZES.append(x)
        x *= 10


def main():

    # build argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='chaining', action='store_true')
    parser.add_argument('-o', dest='open_addressing', action='store_true')
    parser.add_argument('-b', dest='both', action='store_true')
    args = parser.parse_args()

    init()

    if args.chaining or args.open_addressing:
        hash_tables = []
        for ts in TABLE_SIZES:
            for lf in LOAD_FACTORS:
                if args.chaining:
                    hash_tables.append(HashTableChaining(ts, lf))
                elif args.open_addressing:
                    hash_tables.append(HashTableAddressing(ts, lf))
        run_tests(hash_tables)

    elif args.both:
        hash_tables_chaining = []
        hash_tables_addressing = []
        for ts in TABLE_SIZES:
            for lf in LOAD_FACTORS:
                hash_tables_chaining.append(HashTableChaining(ts, lf))
                hash_tables_addressing.append(HashTableAddressing(ts, lf))
        run_tests(hash_tables_chaining)
        run_tests(hash_tables_addressing)

    out.close()


def run_tests(hash_tables):
    insertion_test(hash_tables)
    print(file=out)
    search_test(hash_tables)
    print(file=out)
    deletion_test(hash_tables)
    print(file=out)
    mem_test(hash_tables)
    print(file=out)


def insertion_test(hash_tables):
    title = get_title(hash_tables)
    all_graph_data = []
    insertion_time_by_load_factor = {}
    print('{:^60}'.format('INSERTION (' + title +')'), file=out)
    table_div()
    print('{:10}'.format('LENGTH') +
          '{:8}'.format('LF') +
          '{:20}'.format('START_INSERTIONS') +
          'TIME', file=out)
    table_div()
    avg_insert_times = []
    for ht in hash_tables:
        start_insertions = ht.TOTAL_INSERTIONS
        insert_times = []
        graph_data = None

        try:
            tmp = insertion_time_by_load_factor[ht.ARR_LENGTH]
        except:
            insertion_time_by_load_factor.update({ht.ARR_LENGTH: []})

        if len(all_graph_data) == 0:
            graph_data = GraphData(ht.LOAD_FACTOR)
        else:
            for g in all_graph_data:
                if g.lf == ht.LOAD_FACTOR:
                    graph_data = g
                    break
        if graph_data is None:
            graph_data = GraphData(ht.LOAD_FACTOR)

        for i in range(NUM_TESTS):
            rand_string = gen_random_string()
            start_insert_time = time.time()
            ht.insert(rand_string)
            end_insert_time = time.time()
            insert_time = end_insert_time - start_insert_time
            insert_times.append(insert_time)
            ht.remove(rand_string)

        avg_insert_time = avg(insert_times)
        avg_insert_times.append(avg_insert_time)

        graph_data.sizes.append(ht.ARR_LENGTH)
        graph_data.avg_times.append(avg_insert_time)

        if len(all_graph_data) < len(LOAD_FACTORS):
            all_graph_data.append(graph_data)

        print('{:<10}'.format(ht.ARR_LENGTH) +
              '{:<8}'.format(ht.LOAD_FACTOR) +
              '{:<20}'.format(start_insertions) +
              '{:<20}'.format(avg_insert_time), file=out)
    table_div()

    # Data for plotting
    load_factors = []

    for g in all_graph_data:
        load_factors.append(g.lf)
        for i in range(len(g.sizes)):
            insertion_time_by_load_factor[g.sizes[i]].append(g.avg_times[i]/1000000)

    fig, ax = plt.subplots()

    # multiple line plot
    leg = []
    for key in insertion_time_by_load_factor:
        ax.plot(load_factors, insertion_time_by_load_factor[key])
        leg.append(key)

    ax.set(xlabel='load factor', ylabel='Time (µs)', title='Insertions (' + title +')')
    plt.legend(leg, loc='upper left')

    plt.show()
    fig.savefig("imgs/insertion-" + title.lower() + ".png")


def search_test(hash_tables):
    title = get_title(hash_tables)
    all_graph_data = []
    search_time_by_load_factor = {}
    print('{:^60}'.format('SEARCH (' + title +')'), file=out)
    table_div()
    print('{:10}'.format('LENGTH') +
          '{:8}'.format('LF') +
          'TIME', file=out)
    table_div()

    for ht in hash_tables:
        if not ht.is_empty():
        # if ht.LOAD_FACTOR > 0:
            graph_data = None
            try:
                tmp = search_time_by_load_factor[ht.ARR_LENGTH]
            except:
                search_time_by_load_factor.update({ht.ARR_LENGTH: []})

            if len(all_graph_data) == 0:
                graph_data = GraphData(ht.LOAD_FACTOR)
            else:
                for g in all_graph_data:
                    if g.lf == ht.LOAD_FACTOR:
                        graph_data = g
                        break

            if graph_data is None:
                graph_data = GraphData(ht.LOAD_FACTOR)

            search_times = []
            for i in range(NUM_TESTS):
                search_string = ht.get_random_val()
                start_search_time = time.time()
                ht.lookup(search_string)
                end_search_time = time.time()
                search_times.append(end_search_time - start_search_time)

            avg_search_time = avg(search_times)

            graph_data.sizes.append(ht.ARR_LENGTH)
            graph_data.avg_times.append(avg_search_time)
            if len(all_graph_data) < len(LOAD_FACTORS)-1:
                all_graph_data.append(graph_data)

            print('{:<10}'.format(ht.ARR_LENGTH) +
                  '{:<8}'.format(ht.LOAD_FACTOR) +
                  '{:<20}'.format(avg_search_time), file=out)
    table_div()

    # Data for plotting
    load_factors = []

    for g in all_graph_data:
        load_factors.append(g.lf)
        for i in range(len(g.sizes)):
            search_time_by_load_factor[g.sizes[i]].append(g.avg_times[i]/1000000)

    fig, ax = plt.subplots()

    # multiple line plot
    leg = []
    for key in search_time_by_load_factor:
        ax.plot(load_factors, search_time_by_load_factor[key])
        leg.append(key)

    ax.set(xlabel='load factor', ylabel='Time (µs)', title='Search (' + title + ')')
    plt.legend(leg, loc='upper left')

    plt.show()
    fig.savefig("imgs/search-" + title.lower() + ".png")


def deletion_test(hash_tables):
    title = get_title(hash_tables)
    all_graph_data = []
    delete_time_by_load_factor = {}
    print('{:^60}'.format('DELETE (' + title + ')'), file=out)
    table_div()
    print('{:10}'.format('LENGTH') +
          '{:8}'.format('LF') +
          'TIME', file=out)
    table_div()

    for ht in hash_tables:
        if not ht.is_empty():
            graph_data = None
            try:
                tmp = delete_time_by_load_factor[ht.ARR_LENGTH]
            except:
                delete_time_by_load_factor.update({ht.ARR_LENGTH: []})

            if len(all_graph_data) == 0:
                graph_data = GraphData(ht.LOAD_FACTOR)
            else:
                for g in all_graph_data:
                    if g.lf == ht.LOAD_FACTOR:
                        graph_data = g
                        break

            if graph_data is None:
                graph_data = GraphData(ht.LOAD_FACTOR)

            delete_times = []
            for i in range(NUM_TESTS):
                delete_string = ht.get_random_val()
                start_delete_time = time.time()
                ht.remove(delete_string)
                end_delete_time = time.time()
                delete_times.append(end_delete_time - start_delete_time)

            avg_delete_time = avg(delete_times)

            graph_data.sizes.append(ht.ARR_LENGTH)
            graph_data.avg_times.append(avg_delete_time)
            if len(all_graph_data) < len(LOAD_FACTORS) - 1:
                all_graph_data.append(graph_data)

            print('{:<10}'.format(ht.ARR_LENGTH) +
                  '{:<8}'.format(ht.LOAD_FACTOR) +
                  '{:<20}'.format(avg_delete_time), file=out)
    table_div()

    # Data for plotting
    load_factors = []

    for g in all_graph_data:
        load_factors.append(g.lf)
        for i in range(len(g.sizes)):
            delete_time_by_load_factor[g.sizes[i]].append(g.avg_times[i]/1000000)

    fig, ax = plt.subplots()

    # multiple line plot
    leg = []
    for key in delete_time_by_load_factor:
        ax.plot(load_factors, delete_time_by_load_factor[key])
        leg.append(key)

    ax.set(xlabel='load factor', ylabel='Time (µs)', title='Delete (' + title + ')')
    plt.legend(leg, loc='upper left')

    plt.show()
    fig.savefig("imgs/delete-" + title.lower() + ".png")


def mem_test(hash_tables):
    title = get_title(hash_tables)
    all_graph_data = []
    mem_size_by_load_factor = {}
    print('{:^60}'.format('MEMORY (' + title +')'), file=out)
    table_div()
    print('{:10}'.format('LENGTH') + '{:8}'.format('LF') + '{:17}'.format('MEMORY'), file=out)
    table_div()

    for ht in hash_tables:
        graph_data = None
        try:
            tmp = mem_size_by_load_factor[ht.ARR_LENGTH]
        except:
            mem_size_by_load_factor.update({ht.ARR_LENGTH: []})

        if len(all_graph_data) == 0:
            graph_data = GraphData(ht.LOAD_FACTOR)
        else:
            for g in all_graph_data:
                if g.lf == ht.LOAD_FACTOR:
                    graph_data = g
                    break

        if graph_data is None:
            graph_data = GraphData(ht.LOAD_FACTOR)

        mem_size = ht.get_mem_size()

        graph_data.sizes.append(ht.ARR_LENGTH)
        graph_data.mem_sizes.append(mem_size)
        if len(all_graph_data) < len(LOAD_FACTORS):
            all_graph_data.append(graph_data)

        print('{:<10}'.format(ht.ARR_LENGTH) +
              '{:<8}'.format(ht.LOAD_FACTOR) +
              '{:<17}'.format(mem_size) +
              '{:<20}'.format(""), file=out)
    table_div()

    # Data for plotting
    load_factors = []

    for g in all_graph_data:
        load_factors.append(g.lf)
        for i in range(len(g.sizes)):
            mem_size_by_load_factor[g.sizes[i]].append(g.mem_sizes[i]/1000000)

    fig, ax = plt.subplots()
    width = 0.35
    # multiple line plot
    leg = []
    for key in mem_size_by_load_factor:
        ax.plot(load_factors, mem_size_by_load_factor[key])
        # ax.bar(load_factors, mem_size_by_load_factor[key], width, label=key)

        leg.append(key)

    title = get_title(hash_tables)

    ax.set(xlabel='load factor', ylabel='Size (Mb)', title='Memory Size (' + title +')')
    plt.legend(leg, loc='upper left')

    plt.show()
    fig.savefig("imgs/memsize-" + title.lower() + ".png")


def get_title(hash_tables):
    if isinstance(hash_tables[0], HashTableChaining): return 'Chaining'
    return 'Open-Addressing'


def table_div(): print('{:-^60}'.format(''), file=out)


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


def gen_random_string():
    """
    generate a random string of lowercase letters, 8 characters long
    :return:
    """
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(8))
    return result_str


if __name__ == '__main__':
    main()
