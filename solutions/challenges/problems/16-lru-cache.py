class LRUCache:
    """get returns the value or -1. get and put both count as use.

    Approach: OrderedDict keeps keys in use order. The front is the oldest.
    Time: O(1) for get and put
    Space: O(capacity)
    Alternative: a hash map plus a doubly linked list, built by hand.
    Common bugs: evicting the newest key, or forgetting that get counts as a use.
    """

    def __init__(self, capacity: int):
        from collections import OrderedDict

        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key: int, value: int) -> None:
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)
