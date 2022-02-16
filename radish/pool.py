from typing import Any, List, TypedDict, Callable, Mapping
from radish.exceptions import MethodNotAllowed, NotFound

__all__ = ["Pool"]

class Route(TypedDict):
    path: str
    handler: Callable

class Pool(object):
    def __init__(self, method: str) -> None:
        self.method: str = method
        self.routes: List[Route] = []

    def insert(self, route: str, handler: Callable, **kwargs: dict) -> None:
        route: dict = {"path": route, "handler": handler}
        route.update(kwargs)
        self.routes.append(route)

    def get(self, route: str) -> Route:
        for r in self.routes:
            if r["path"] == route:
                return r
        raise NotFound("Route not found")
    
    def __repr__(self) -> str:
        return f"<Pool method={self.method} routes={self.routes}>"
