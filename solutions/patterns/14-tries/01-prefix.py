
class Book:
    """A trie of letters. search is true only for a whole inserted word.

    Approach: one child map per node, and a mark on the last letter.
    Time: O(length) to insert or search
    Space: O(total letters)
    Alternative: a set of the words, which does not share prefixes.
    Common bugs: returning true for a prefix that was never inserted.
    """

    def __init__(self) -> None:
        self.children: dict[str, Book] = {}
        self.word = False

    def insert(self, text: str) -> None:
        node = self
        for character in text:
            node = node.children.setdefault(character, Book())
        node.word = True

    def search(self, text: str) -> bool:
        node = self
        for character in text:
            if character not in node.children:
                return False
            node = node.children[character]
        return node.word


def stored(word: str) -> bool:
    book = Book()
    book.insert(word)
    return book.search(word)


def shared_prefix(words: list[str]) -> str:
    """Longest prefix shared by every word.

    Approach: walk the first word until another word disagrees or ends.
    Time: O(total letters)
    Space: O(1) beyond the answer
    Alternative: insert every word in a trie and walk while a node has one child.
    Common bugs: assuming the first word is the shortest.
    """
    if not words:
        return ""
    prefix = words[0]
    for word in words[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


def starts_with(book: Book, text: str) -> bool:
    node = book
    for character in text:
        if character not in node.children:
            return False
        node = node.children[character]
    return True


def has_prefix() -> bool:
    book = Book()
    book.insert("hi")
    return starts_with(book, "h")
