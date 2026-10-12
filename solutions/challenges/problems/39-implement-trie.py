
class Trie:
    """insert, search, and starts_with.

    Approach: a child map on each node and a mark for the end of a word.
    Time: O(length) per call
    Space: O(total letters)
    Alternative: a set of words, which cannot answer starts_with without a scan.
    Common bugs: search returning true for a prefix that was never inserted as its own word.
    """

    def __init__(self) -> None:
        self.children: dict[str, Trie] = {}
        self.end = False

    def insert(self, word: str) -> None:
        node = self
        for character in word:
            node = node.children.setdefault(character, Trie())
        node.end = True

    def _walk(self, text: str):
        node = self
        for character in text:
            if character not in node.children:
                return None
            node = node.children[character]
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.end

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
