ht = None


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


class HashTable:

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
    global ht
    ht = HashTable()
    ht.insert('foo')
    print(ht.lookup('foo'))


if __name__ == '__main__':
    main()
