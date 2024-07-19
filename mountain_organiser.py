from __future__ import annotations

from mountain import Mountain
from algorithms.mergesort import mergesort, merge
from algorithms.binary_search import binary_search

class MountainOrganiser:

    def __init__(self) -> None:
        """
        Complesxity: O(1) to initialise a list
        """
        self.m_list = []


    def cur_position(self, mountain: Mountain) -> int:
        """
        Finds the rank of the provided mountain given all mountains included so far.
        Raises KeyError if this mountain hasn't been added yet.

        Complexity: Best-case is O(1) if the mountain we are finding is the middle of m_list. Worst-case is O(log(n)), where n is
        the length of the list. This occurs if the mountain's length is the smallest or largest in the list, so log(n)
        recursive calls are done.
        """
        return binary_search(self.m_list, mountain)


    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Adds a list of mountains to the organiser

        Complexity:
         Best case: O(mlog(m)), where m is the length of the list mountains and there are no existing mountains in
         m_list so far, so only mergesort is called.

         Worst case: O(mlog(m)+n), where m is the length of the list mountains and n is the number of elements
         in m_list so far. O(mlog(m)) is the time complexity of mergesort in sorting the new mountains being added.
         Since this sorted list of mountains is then merged with the existing list of length n,
         and merge time complexity is  O(k), k = len(l1)+len(l2), then the merge time complexity is
         O(m+n).
         So overall worst time complexity is O(mlog(m)+m+n) = O(mlog(m)+n).
        """
        # m_list should always be sorted already
        # add to list: just use mergesort on mountains, then merge mountains and m_list
        if len(self.m_list) is None:
            self.m_list = mergesort(mountains)
        else:
            add_list = mergesort(mountains)
            self.m_list = merge(add_list, self.m_list)




