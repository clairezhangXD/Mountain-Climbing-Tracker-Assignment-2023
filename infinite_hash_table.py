from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        assert(self.TABLE_SIZE > 0)
        self.count = 0
        self.table = ArrayR(self.TABLE_SIZE)
        self.level = 0


    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)  # returns hash position within the current level
        return self.TABLE_SIZE-1  # returns hash position on the last level (the end of the table)

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Best case: O(1) when the key is on level 0 of the hash table, so there is direct access to the key, value pair
        Worst case: O(N) where N is the length of the key, the key,value pair is set in Nth level of the hash
         table
        """

        copy_table = self.table
        self.level = 0
        while self.level <= len(key)-1:
            pos = self.hash(key)
            if self.table[pos] is None:
                self.table = copy_table
                raise KeyError("Key doesn't exist!")
            elif self.table[pos][0] == key:
                self.table = copy_table
                return self.table[pos][1]
            else:
                self.table[pos] = self.table[pos][1]
                self.level += 1


    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Best case: O(1), when the (key, value) pair is being set to a position on level 0 of the hash table.
        Worst case: O(N^2), where N is the length of the key and the key is set in the Nth level of the hash table.
        At each level, the key is sliced using Python's string slice, which makes a copy of the given string,
        which takes N iterations, thus O(N*N) = O(N^2).
        """
        # level 0
        copy_table = self.table
        self.level = 0
        pos = self.hash(key)

        while self.level <= len(key)-1: # next levels
            pos = self.hash(key)
            if self.table[pos] is None:
                self.table[pos] = (key, value)
                self.count += 1
                self.table = copy_table
                return
            elif self.table[pos][0] == key:
                self.table[pos] = (key, value)
                self.table = copy_table
                return
            else:
                if type(self.table[pos]) is tuple:  # there is a key-value pair already, so need to slice key and
                    # reinsert it
                    existing_key, existing_value = self.table[pos]
                    self.table[pos] = [key[:self.level+1], ArrayR(self.TABLE_SIZE)]
                    self.table = self.table[pos][1]
                    self.level += 1
                    pos_existing_key = self.hash(existing_key)
                    self.table[pos_existing_key] = (existing_key, existing_value)
                else:
                    self.table = self.table[pos][1]
                    self.level += 1


        # position = self.hash(key)
        #
        # if self.table[position] is None:
        #     self.table[position] = ArrayR(self.TABLE_SIZE)
        #
        # # Attempt to find the key in our linked list
        # for index, item in enumerate(self.table[position]):
        #     if item[0] == key:
        #         # If found update the data
        #         self.table[position][index] = (key, value)
        #         return
        #
        # # Otherwise insert it at the beginning
        # self.table[position].insert(0, (key, value))
        # self.count += 1


    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Best case: O(1), when the (key,value) pair being deleted is in level 0 of the hash table.

        Worst case: O(N(N+M)), when table can be collapsed all the way to level 0.
        Further Explanation...
        Deleting the (key, value) pair takes O(N+N), where N is the length of the list returned by
        get_location (number of levels).
        Python's list slice makes a copy of the given array, which takes N iterations.
        Then, the table will need to be indexed until the sequence ends to reach the key, which takes N iterations.
        Simplified, this takes O(N) time.

        Collapsing the table takes O(N*(N+N+M)) where N is the length of the list returned by get_location (number of
        levels) and M is the length of the current hash table. For each level of the table, N+N+M operations
        are performed. Python's list slice makes a copy of the given array, which takes N iterations.
        Then, the table will need to be indexed until the get_location sequence ends to reach the hash
        table we need to search, which also takes N iterations. Then that hash table is linearly searched M times before
        deducing whether or not the hash table can be collapsed.
        Simplified, this takes O(N*(N+M)) time.

        Thus worst case is O(delete+collapsing) = O(N(N+M))
        """
        # delete
        copy_table = self.table
        location_list = self.get_location(key)
        level = len(location_list)-1
        for i in location_list[:level]:
            self.table = self.table[i][1]  # set self.table as table of current level
        self.table[location_list[level]] = None  # delete the (key,value)
        self.count -= 1

        # collapsing
        tuple_count = 0
        while level >= 1:
            self.table = copy_table
            for i in location_list[:level]:
                self.table = self.table[i][1]
            key_count = 0  # counts keys in current table
            for element in self.table:
                if element is not None:
                    if type(element) is tuple:
                        remaining_tuple = element
                        tuple_count += 1
                    else:  # only key remaining
                        key_count += 1
                if key_count == 1 and tuple_count == 0 or tuple_count > 1:  # don't collapse table containing key
                    # with table (table could contain more tuples) or other tuples
                    self.table = copy_table
                    return
            if tuple_count == 1:  # collapse table containing 1 tuple or 1 key with table (that contains 1 tuple)
                self.table = remaining_tuple
            level -= 1

        self.table = copy_table

        # level 0
        if level == 0:
            if tuple_count == 0:
                return
            self.table[location_list[level]] = remaining_tuple


    def __len__(self) -> int:
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key) -> list:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.

        Best case: O(1), when the key is in level 0 of the hash table, so no need to traverse the hash table.
        Worst case: O(N), where N is the length of the key and the key is set in the Nth level of the hash table.
        To obtain every index required to access this key, the hash table will need to be traversed N times.
        """

        copy_table = self.table
        self.level = 0
        location_list = []

        while self.level <= len(key):
            pos = self.hash(key)
            if type(self.table) is int or self.table[pos] is None:  # self.table is an int when it is
                # value of different key
                self.table = copy_table
                raise KeyError("Key doesn't exist!")
            elif self.table[pos][0] == key and type(self.table[pos]) is tuple:
                location_list.append(pos)
                self.table = copy_table
                return location_list
            else:
                location_list.append(pos)
                self.table = self.table[pos][1]
                self.level += 1

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True


