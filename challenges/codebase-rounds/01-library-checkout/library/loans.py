def checkout(patron: str, title: str, loans: list[tuple[str, str]] = []) -> list[tuple[str, str]]:  # noqa: B006
    loans.append((patron, title))
    return loans
