from __future__ import annotations
from typing import TypeVar

T = TypeVar("T")

def binary_search(l: list[T], item: T) -> int:
    """
    Utilise the binary search algorithm to find the index where a particular element is stored.
    Raises KeyError when item is not in the list

    :return: The index at which this item is located

    :complexity:
    Best Case Complexity: O(1), when middle index contains item.
    Worst Case Complexity: O(log(N)), where N is the length of l.
    """
    return _binary_search_aux(l, item, 0, len(l))

def _binary_search_aux(l: list[T], item: T, lo: int, hi: int) -> int:
    """
    Auxilliary method used by binary search.
    lo: smallest index where the return value could be.
    hi: largest index where the return value could be.
    """
    # Edited code: added if statement and raise KeyError
    if lo == hi:
        if l[lo] == item:
            return lo
        raise KeyError("Item not in list!")

    mid = (hi + lo) // 2
    if l[mid] > item:
        # Item would be before mid
        return _binary_search_aux(l, item, lo, mid)
    elif l[mid] < item:
        # Item would be after mid
        return _binary_search_aux(l, item, mid+1, hi)
    elif l[mid] == item:
        return mid

    raise ValueError(f"Comparison operator poorly implemented {item} and {l[mid]} cannot be compared.")
