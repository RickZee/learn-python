def has_cycle(head) -> bool:
    """True when a node points at an earlier node.

    Approach: Floyd. Slow steps once, fast steps twice. They meet only in a cycle.
    Time: O(n)
    Space: O(1)
    Alternative: a set of seen nodes.
    Common bugs: moving fast before checking that fast.next exists.
    """
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
