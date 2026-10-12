def is_valid(s: str) -> bool:
    """True when brackets nest and close in order. An empty string is valid.

    Approach: push openers, and each closer must match the opener on top.
    Time: O(n)
    Space: O(n)
    Alternative: repeatedly delete "()", "[]", and "{}" until nothing changes.
    Common bugs: popping an empty stack, or matching a closer with the wrong opener.
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for character in s:
        if character in "([{":
            stack.append(character)
        elif not stack or stack.pop() != pairs.get(character):
            return False
    return not stack
