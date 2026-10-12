
def middle_value(head) -> int:
    """Return the middle value. On an even length, return the second middle.

    Approach: slow steps once and fast steps twice.
    Time: O(n)
    Space: O(1)
    Alternative: count the nodes, then walk half way.
    Common bugs: stopping on the first of two middle nodes.
    """
    slow = fast = head
    while fast is not None and fast.nxt is not None:
        slow = slow.nxt
        fast = fast.nxt.nxt
    return slow.value


def length(head) -> int:
    count = 0
    while head is not None:
        count += 1
        head = head.nxt
    return count
