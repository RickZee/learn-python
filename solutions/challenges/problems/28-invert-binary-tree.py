
def invert_tree(root):
    """Swap every left and right child.

    Approach: swap, then invert both sides.
    Time: O(n)
    Space: O(n) for the call stack
    Alternative: the same swap with a queue.
    Common bugs: swapping after the recursive calls, so you invert the original sides twice.
    """
    if root is None:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
