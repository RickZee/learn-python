def checkout(
    patron: str, title: str, loans: list[tuple[str, str]] | None = None
) -> list[tuple[str, str]]:
    if loans is None:
        loans = []
    loans.append((patron, title))
    return loans
