def to_values_one(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def to_list(values: list[int]):
    head = None
    tail = None
    for value in values:
        node = Node(value)  # noqa: F821
        if head is None:
            head = node
        else:
            tail.next = node
        tail = node
    return head


def to_values(head) -> list[int]:
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def length(head) -> int:
    count = 0
    while head is not None:
        count += 1
        head = head.next
    return count
