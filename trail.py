from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from typing import TYPE_CHECKING, Union
from typing import List

from data_structures.linked_stack import LinkedStack

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.path_follow.store

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail 

    mountain_list = [Mountain] # use list

    def remove_mountain(self) -> TrailStore: 
        """Removes the mountain at the beginning of this series."""

        return self.following.store # Trail is following the mountain, so returns store of that trail


    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        # self.store = TrailSeries(mountain,Trail(self))
        # return self.store

        return TrailSeries(mountain, Trail(self))


    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        # self.path_top = None
        # self.path_bottom = None
        # self.store = TrailSplit(Trail(None),Trail(None),self.following) # top and bottom is empty, joined by following path
        # return self.store

        return TrailSplit(Trail(None), Trail(None), Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        # self.m_current = self.mountain
        # self.path_follow = TrailSeries(mountain,Trail(self.following))
        # self.store = TrailSeries(self.m_current,Trail(self.path_follow))
        # return self.store

        return TrailSeries(self.mountain, Trail(TrailSeries(mountain, self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        # self.new_branch_before = TrailSplit(Trail(None),Trail(None),self.following)
        # self.store = TrailSeries(self.mountain,self.new_branch_before)
        # return self.store

        return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:
    store: TrailStore = None


    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        return Trail(TrailSplit(Trail(None), Trail(None), self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """
        Follow a path and add mountains according to a personality.
        Complexity: The best-case is O(1) if there is initially nothing in store, so it can return a value immediately. In the 
        worst-case, it is O(n) where n is the number of mountains in the trail. This will occur when there is only one long 
        trail and no splits as all the mountains are in the same Trail.
        """
        copy_og_store = self.store
        stack_follow = LinkedStack()
        while True:

            if isinstance(self.store, TrailSeries):  # add mountain, then set following trail store as current store
                personality.add_mountain(self.store.mountain)
                self.store = self.store.following.store

            elif isinstance(self.store, TrailSplit):  # based on selected branch, set that branch's trail store as
                # current trail store. Store path following the split in stack
                is_top = personality.select_branch(self.store.path_top, self.store.path_bottom)
                stack_follow.push(self.store.path_follow.store)
                if is_top:
                    self.store = self.store.path_top.store
                else:
                    self.store = self.store.path_bottom.store

            else:  # store is None
                if stack_follow.is_empty():
                    self.store = copy_og_store  # restarts the Trail, so that next time follow_path is called,
                    # the instance stores the entire trail, not None
                    break  # trail end
                else:
                    self.store = stack_follow.pop()  # Last trail in is first current store


    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        pass

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        pass
