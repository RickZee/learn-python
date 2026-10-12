def reverse_list(head):
    """Reverse the nodes and return the new head. An empty list stays empty.

    Approach: walk once, pointing each next link at the previous node.
    Time: O(n)
    Space: O(1)
    Alternative: recursion, which uses O(n) stack space.
    Common bugs: losing the rest of the list before you store the next node.
    """
    previous = None
    while head is not None:
        nxt = head.next
        head.next = previous
        previous = head
        head = nxt
    return previous
