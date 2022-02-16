from typing import Tuple


def throw(expr: str, msg: str) -> None:
    if not expr:
        raise Exception(msg)

def is_wildcard(c: str) -> bool:
    assert len(c) == 1, "Length of wildcard is only 1, please provide a name"
    return c == ":" or c == "*"


def split_from_first_slash(path: str) -> Tuple[str, str]:
    i = 0
    while i < len(path) and path[i] != "/":
        i += 1
    return (path[0:i], path[i:])

def longest_common_prefix(a: str, b: str) -> int:
    i = 0
    length = min(len(a), len(b))
    while i < length and a[i] == b[i]:
        i += 1
    return i

