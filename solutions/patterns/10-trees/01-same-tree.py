
def preorder(node) -> list[int]:
    if node is None:
        return []
    return [node.value] + preorder(node.left) + preorder(node.right)


def same_tree(left, right) -> bool:
    """True when both trees match in shape and value.

    Approach: both empty matches; one empty does not; otherwise compare the value and both sides.
    Time: O(n)
    Space: O(n) for the call stack
    Alternative: compare the two preorder walks, using a marker for empty children.
    Common bugs: treating a missing child on the left the same as a value on the right.
    """
    if left is None or right is None:
        return left is right
    return (
        left.value == right.value
        and same_tree(left.left, right.left)
        and same_tree(left.right, right.right)
    )


def inorder(node) -> list[int]:
    if node is None:
        return []
    return inorder(node.left) + [node.value] + inorder(node.right)
