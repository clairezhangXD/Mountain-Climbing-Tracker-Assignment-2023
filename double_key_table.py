from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        """
        Complexity: The best-case=worst is O(1) no matter the input. The method only needs to
        initialise the array, count, top and bottom sizes attributes.
        """
        self.top_size = self.TABLE_SIZES
        self.bottom_size = self.TABLE_SIZES

        if sizes is not None:
            self.top_size = sizes
        if internal_sizes is not None:
            self.bottom_size = internal_sizes
        self.top_size_index = 0
        self.array = ArrayR(self.top_size[self.top_size_index])
        self.count = 0


    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value


    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.

        Complexity: The best case is O(len(key)+len(key))=O(len(key)) and happens when the key is found in
        its initial hash value positions.
        The worst-case is O(len(key)+n+m),where n is the size of outer table and m is the size of the inner table.
        This occurs when the function has to probe the entire outer table and inner table to find empty slots,
         or to find that the key doesn't exist in the table.
        """
        pos1 = self.hash1(key1)

        for _ in range(self.table_size):
            if self.array[pos1] is None:

                if is_insert:
                    if key2 is None:  # __delitem__ reinserting
                        return pos1

                    # create internal table
                    internal_array = LinearProbeTable(self.bottom_size)
                    internal_array.hash = lambda k: self.hash2(k, internal_array)
                    self.array[pos1] = [key1, internal_array]
                    pos2 = internal_array._linear_probe(key2, is_insert)
                    return pos1, pos2
                else:
                    raise KeyError(key1)

            elif self.array[pos1][0] == key1:
                if key2 is None:  # for keys()
                    return pos1
                internal_array = self.array[pos1][1]
                pos2 = internal_array._linear_probe(key2, is_insert)
                return pos1, pos2

            else:
                pos1 = (pos1+1) % self.table_size

        if is_insert:
            raise FullError("Table is full!")
        else:
            raise KeyError(key1)


    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        Complexity: Best-case is O(1) if the table is empty. Worst-case is O(n), where n is the size of the internal hash table.
        This occurs when the internal array is completely full, so it has to iterate over n elements.
        """
        if key is None:
            for item in self.array:
                if item is not None:
                    yield item[0]

        else:
            pos1 = self._linear_probe(key, None, False)
            internal_array = self.array[pos1][1]
            for item in internal_array.array:
                if item is not None:
                    yield item[0]


    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        Complexity: Best-case is O(1) if the table is empty or the key is found at the first index. 
        Worst-case is O(n), where n is the size of the internal hash table. This occurs when the internal array is 
        completely full, so it has to probe n times before finding the matching key.
        """
        keys_list = []

        if key is None:
            for item in self.array:
                if item is not None:
                    keys_list.append(item[0])

        else:
            pos1 = self._linear_probe(key, None, False)
            internal_array = self.array[pos1][1]
            for item in internal_array.array:
                if item is not None:
                    keys_list.append(item[0])

        return keys_list

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        Complexity: Best-case is O(1) if the table is empty or the key is found at the first index. 
        Worst-case is O(n), where n is the size of the internal hash table. This occurs when the internal array is 
        completely full, so it has to probe n times before finding the matching key.
        """
        if key is None:
            for item1 in self.array:
                if item1 is not None:
                    internal_array = item1[1]
                    for item2 in internal_array.array:
                        if item2 is not None:
                            yield item2[1]

        else:
            pos1 = self._linear_probe(key, None, False)
            internal_array = self.array[pos1][1]
            for item in internal_array.array:
                if item is not None:
                    yield item[1]


    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        Complexity: Best-case is O(1) if the table is empty or the key is found at the first index. 
        Worst-case is O(n), where n is the size of the internal hash table. This occurs when the internal array is 
        completely full, so it has to probe n times before finding the matching key.
        """
        values_list = []

        if key is None:
            for item1 in self.array:
                if item1 is not None:
                    internal_array = item1[1]
                    for item2 in internal_array.array:
                        if item2 is not None:
                            values_list.append(item2[1])

        else:
            pos1 = self._linear_probe(key, None, False)
            internal_array = self.array[pos1][1]
            for item in internal_array.array:
                if item is not None:
                    values_list.append(item[1])

        return values_list


    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Complexity: Best-case is O(1) if the table is empty or the key is found at the first index. 
        Worst-case is O(n), where n is the size of the internal hash table. This occurs when the internal array is 
        completely full, so it has to probe n times before finding the matching key.
        """
        pos1, pos2 = self._linear_probe(key[0], key[1], False)
        return self.array[pos1][1][key[1]]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Complexity: Best-case is O(1) if the keys are distributed evenly and there are no collisions. The worst-case is O(n), 
        where n is the size of the internal table. This will occur if the table is full and we have to probe every slot before
        finding an empty one.
        """
        pos1, pos2 = self._linear_probe(key[0], key[1], True)
        internal_array = self.array[pos1][1]
        try:
            internal_array[key[1]]
        except KeyError:  # position in internal table is None, means new pair
            self.count += 1

        internal_array[key[1]] = data  # calls internal array's __setitem__, so should do internal rehash

        key1_counter = 0
        for item in self.array:
            if item is not None:
                key1_counter += 1
        if key1_counter > self.table_size / 2:
            self._rehash()


    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Complexity: Best-case is O(1) where the pair is removed from the first index of the internal array. Worst-case is O(m+n), 
        where m is the number of slots in the hash table, and n is the number of clusters. This will occur when the pair we are 
        deleting is the only pair in the internal array, and all remaining clusters have to be  reinserted.
        """
        pos1, pos2 = self._linear_probe(key[0], key[1], False)

        # Remove the element
        # use internal table __delitem__
        # if only pair, del internal_array and reinsert
        # else, only del key2
        internal_array = self.array[pos1][1]
        if len(internal_array) > 1:
            del internal_array[key[1]]
            self.count -= 1
        else:
            # del bottom-level table and re-insert top-level table cluster
            self.array[pos1] = None
            self.count -=1

            # Start moving over the cluster
            position = (pos1 + 1) % self.table_size
            while self.array[position] is not None:
                key1 = self.array[position][0]
                internal_array = self.array[position][1]
                self.array[position] = None
                # Reinsert
                newpos = self._linear_probe(key1, None, True)
                self.array[newpos] = [key1, internal_array]
                position = (position + 1) % self.table_size


    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_array = self.array
        self.top_size_index += 1
        if self.top_size_index == len(self.top_size):
            # Cannot be resized further.
            return
        self.array = ArrayR(self.top_size[self.top_size_index])
        self.count = 0

        for item1 in old_array:
            if item1 is not None:
                key1, internal_array = item1
                for item2 in internal_array.array:
                    if item2 is not None:
                        key2, value = item2
                        self[key1, key2] = value  # re-set

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        Complexity: Returning is O(1)
        """
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        Complexity: Returning is O(1)
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        result = ""
        for item in self.array:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result



