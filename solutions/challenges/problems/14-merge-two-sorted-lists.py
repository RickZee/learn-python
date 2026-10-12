def merge_two_lists(list1, list2):
    """Merge two sorted lists into one sorted list. Either input may be empty.

    Approach: a dummy head, then always attach the smaller node.
    Time: O(n + m)
    Space: O(1)
    Alternative: recursion on the smaller head.
    Common bugs: dropping the leftover tail when one list runs out.
    """
    dummy = ListNode()  # noqa: F821
    tail = dummy
    while list1 is not None and list2 is not None:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    tail.next = list1 if list1 is not None else list2
    return dummy.next
