
def is_valid_bst(root) -> bool:
    """True when every left value is smaller and every right value is larger.

    Approach: carry an exclusive low and high bound.
    Time: O(n)
    Space: O(n) for the call stack
    Alternative: an inorder walk must be strictly increasing.
    Common bugs: comparing a node only with its parent, so a deeper node can break the order.
    """

    def walk(node, low: float, high: float) -> bool:
        if node is None:
            return True
        if not low < node.val < high:
            return False
        return walk(node.left, low, node.val) and walk(node.right, node.val, high)

    return walk(root, float("-inf"), float("inf"))
