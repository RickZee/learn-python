
def max_depth(root) -> int:
    """Longest root-to-leaf path, in nodes. Empty is 0.

    Approach: 1 plus the deeper child.
    Time: O(n)
    Space: O(n) for the call stack
    Alternative: level order, counting the levels.
    Common bugs: counting edges instead of nodes.
    """
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
