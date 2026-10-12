
def level_order(root) -> list[list[int]]:
    """Values one depth at a time.

    Approach: a queue. The nodes in the queue at the start of a round are one level.
    Time: O(n)
    Space: O(n)
    Alternative: recursion with the depth as an index into the answer.
    Common bugs: mixing the next level into the list you are still reading.
    """
    if root is None:
        return []
    levels = []
    queue = [root]
    while queue:
        levels.append([node.val for node in queue])
        queue = [child for node in queue for child in (node.left, node.right) if child]
    return levels
