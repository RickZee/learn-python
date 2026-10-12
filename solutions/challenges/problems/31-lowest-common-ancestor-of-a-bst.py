
def lowest_common_ancestor(root, p: int, q: int) -> int:
    """Value of the lowest common ancestor in a BST.

    Approach: walk down. The split between p and q is the ancestor.
    Time: O(n)
    Space: O(1)
    Alternative: parent pointers and two sets of ancestors.
    Common bugs: returning as soon as one value matches, before checking the other side.
    """
    node = root
    while node is not None:
        if p < node.val and q < node.val:
            node = node.left
        elif p > node.val and q > node.val:
            node = node.right
        else:
            return node.val
    raise ValueError("both values must exist")
