class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_k_lists(lists):
    """Merge k sorted lists.

    Approach: a heap of the current head of each list.
    Time: O(n log k)
    Space: O(k)
    Alternative: merge the lists two at a time.
    Common bugs: pushing nodes that cannot be ordered, because a node is not comparable.
    """
    import heapq

    heap = []
    for index, node in enumerate(lists):
        if node is not None:
            heapq.heappush(heap, (node.val, index, node))
    dummy = ListNode()
    tail = dummy
    while heap:
        _, index, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next is not None:
            heapq.heappush(heap, (node.next.val, index, node.next))
    return dummy.next
