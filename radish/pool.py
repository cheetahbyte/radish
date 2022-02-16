from typing import Callable, Tuple
from radish.utils import is_wildcard, longest_common_prefix, split_from_first_slash, throw


class Node:
    def __init__(self, path: str = "", handler: Callable = None, children=dict()) -> None:
        self.children: dict = children
        self.path: str = path
        self.handler: Callable = handler

    def add(self, path: str, handler: Callable) -> None:
        n = self
        i = 0

        while i < len(path) and not is_wildcard(path[i]):
            i += 1
        n = n.merge(path[0:i])
        j: int = i
        while i < len(path):
            if is_wildcard(path[i]):
                if j != i:
                    n = n.insert(path[j:i])
                    j = i
            i += 1

            while i < len(path) and path[i] != "/":
                if is_wildcard(path[i]):
                    raise Exception(
                        f"only one wildcard per path segment is allowed, has: {path[j:i]} in path {path}")
                i += 1

            if path[j] == ":" and i - j == 1:
                raise Exception(
                    f"param must be named with a non-empty name in path {path}")

            n = n.insert(path[j:i])
            j = i

        if j == len(path):
            n.merge("", handler)

        else:
            n.insert(path[j:], handler)

    def find(self, path: str) -> Tuple[Callable, dict]:
        handler = None
        params = dict()

        stack = [
            [self, path, False]
        ]

        i = 0

        while i >= 0:
            n, p, v = stack[i]
            np = None

            if v:
                i -= 1
                if n.path[0] == ":":
                    params[f"{n.path[1:]}"] = None
                continue
            else:
                stack[i][2] = True

            if n.path[0] == "*":
                if len(n.path) > 1:
                    params[f"{n.path[1:]}"] = p
                np = None
            elif n.path[0] == ":":
                _cp, _np = split_from_first_slash(p)
                params[f"{n.path[1:]}"] = _cp
                if _np == "":
                    np = None
                else:
                    np = _np
            elif n.path == p:
                if n.handler == None:
                    if "*" in n.children.keys():
                        np = ""
                    else:
                        i -= 1
                        continue
                else:
                    np = None
            else:
                lcp = longest_common_prefix(n.path, p)
                if lcp != len(n.path):
                    i -= 1
                    continue
                else:
                    np = p[lcp:]

            if np == None:
                handler = n.handler
                break

            c = n.children.get("*")
            if c != None:
                i += 1
                stack.insert(i, [c, np, False])

            if np == "":
                continue

            c = n.children.get(":")
            if c != None:
                i += 1
                stack.insert(i, [c, np, False])

            c = n.children.get(np[0])
            if c != None:
                i += 1
                stack.insert(i, [c, np, False])

        return [handler, params]

    def merge(self, path, handler=None):
        n = self

        if n.path == "" and len(n.children) == 0:
            n.path = path
            n.handler = handler

            return n

        if path == "":
            if n.handler != None:
                raise Exception(
                    f"A handler is already registered for path {n.path}")
            n.handler = handler

            return n

        while True:
            i = longest_common_prefix(path, n.path)

            if i < len(n.path):
                c = Node(n.path[i:], n.handler, n.children)

                n.children = dict()
                n.children[f"{c.path[0]}"] = c
                n.path = path[0:i]
                n.handler = None

            if i < len(path):
                path = path[i:]
                c = n.children.get(path[0])

                if c != None:
                    n = c
                    continue

                c = Node(path, handler)
                n.children[f"{path[0]}"] = c
                n = c
            elif handler != None:
                if n.handler != None:
                    raise Exception(
                        f"a handler is already registered for path {path}")
                n.handler = handler
            break

        return n

    def insert(self, path: str, handler: Callable=None) -> "Node":
        n = self
        
        c = n.children.get(path[0])

        if c != None:
            n = c.merge(path, handler)
        else:
            c = Node(path, handler)
            n.children[f"{path[0]}"] = c
            n = c
        
        return n


