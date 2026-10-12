

def only_parens(s: str) -> bool:
    depth = 0
    for character in s:
        if character == "(":
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def nesting_depth(s: str) -> int:
    depth = 0
    best = 0
    for character in s:
        if character == "(":
            depth += 1
            best = max(best, depth)
        elif character == ")":
            depth -= 1
    return best

def backspace_compare(left: str, right: str) -> bool:
    """True when both strings are equal after applying backspaces. # deletes one character.

    Approach: build each typed result with a stack.
    Time: O(n)
    Space: O(n)
    Alternative: walk both strings from the end, skipping deleted characters.
    Common bugs: deleting from an empty stack by going negative.
    """

    def typed(text: str) -> list[str]:
        stack = []
        for character in text:
            if character == "#" and stack:
                stack.pop()
            elif character != "#":
                stack.append(character)
        return stack

    return typed(left) == typed(right)
