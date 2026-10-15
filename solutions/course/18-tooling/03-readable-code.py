def constant_name(words: str) -> str:
    return "_".join(words.split()).upper()


def snake_case(name: str) -> str:
    pieces = []
    for index, char in enumerate(name):
        if char.isupper() and index > 0:
            pieces.append("_")
        pieces.append(char.lower())
    return "".join(pieces)


def clean_source() -> str:
    return """def calc_total(prices):
    total = 0
    for price in prices:
        total += price
    return total
"""


def rename_report(names: list[str]) -> dict[str, str]:
    report = {}
    for name in names:
        new_name = snake_case(name)
        if new_name != name:
            report[name] = new_name
    return report
