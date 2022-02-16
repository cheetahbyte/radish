from typing import List, Mapping, Callable
from radish.pool import Pool, Route

class Radish:
    """Radish Router"""
    methods: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"]

    def __init__(self, trim_trailing_slash: bool = True) -> None:
        self.pools: Mapping[str, Pool] = {}
        self.trim_trailing_slash: bool = trim_trailing_slash
        for method in self.methods:
            self.pools[method.lower()] = Pool(method)

    def insert(self, method: str, route: str, handler: Callable, **kwargs: dict) -> None:
        """insert a new route into the pool"""
        self.pools[method.lower()].insert(route, handler, **kwargs)

    def get(self, method: str, route: str) -> Callable:
        """get the handler for a route"""
        return self.pools[method.lower()].get(route)

    def __repr__(self) -> str:
        return f"<RadishRouter pools={self.pools}>"
