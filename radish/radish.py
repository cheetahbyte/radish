from typing import List, Mapping, Callable
from radish.pool import Node

class Radish:
    """Radish Router"""
    methods: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"]

    def __init__(self, trim_trailing_slash: bool = True) -> None:
        self.pools: Mapping[str, Node] = {}
        self.trim_trailing_slash: bool = trim_trailing_slash
        for method in self.methods:
            self.pools[method.lower()] = Node()

    def insert(self, method: str, route: str, handler: Callable, **kwargs: dict) -> None:
        """insert a new route into the pool"""
        if route.endswith("/") and len(route) > 1 and self.trim_trailing_slash:
            route = route[:-1]
        self.pools[method.lower()].add(route, handler)

    def get(self, method: str, route: str) -> dict:
        """get the handler for a route"""
        if route.endswith("/") and len(route) > 1 and self.trim_trailing_slash:
            route = route[:-1]
        return self.pools[method.lower()].find(route)

    def __repr__(self) -> str:
        return f"<RadishRouter pools={self.pools}>"
