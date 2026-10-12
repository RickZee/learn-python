def is_ok(code: int) -> bool:
    match code:
        case 200:
            return True
        case _:
            return False


def http_label(code: int) -> str:
    match code:
        case 200:
            return "ok"
        case 404:
            return "missing"
        case 500 | 502 | 503:
            return "server"
        case _:
            return "other"


def client_or_other(code: int) -> str:
    match code:
        case 400 | 404:
            return "client"
        case _:
            return "other"
