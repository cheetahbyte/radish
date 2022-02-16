from ast import Call
import re
from typing import Any, Callable, List, Mapping, TypedDict

from radish.exceptions import MethodNotAllowed, NotFound
from radish.typings import Route, StoredRoute, RoutingPriority
from radish.utils import make_route, matches, conv_wildcards

__all__ = ["Pool"]




# regex for dynamic route parameters
dyn_regex = r"(\:(?P<var>[a-zA-Z]+)(?:\|(?P<var_type>[a-z]+))?)"
wld = r"(?P<wildcard>\*.*)"

group = r"(:(?P<paramname>[a-zA-Z]+)(?:\|(?P<paramtype>[a-z]+))?)"

wild_card = r"\/?(?P<wildcard>\*[\da-zA-Z-]+)\/?"
wild_card_replace = r""
class Pool(object):
    def __init__(self, method: str) -> None:
        self.method: str = method
        self.routes: List[StoredRoute] = []

    def insert(self, path: str, handler: Callable, **kwargs) -> None:
        route: StoredRoute = {"path": path, "handler": handler, "vars": [], "params": {}}
        # check if route is dynamic
        route["dynamic"] = True if (":" in path or "*" in path) else False
        if route["dynamic"]:
            dyn_matches = [m.groupdict() for m in re.finditer(dyn_regex, path, re.IGNORECASE)]
            wld_matches = [conv_wildcards(m.groupdict()) for m in re.finditer(wld, path, re.IGNORECASE)]
            variables = dyn_matches + wld_matches
            route["vars"] = variables
            for val in route["vars"]:
                pass


    def get(self, path: str) -> Route:
        route: Route = {"path": path, "handler": None, "params": {}}
        for r in self.routes:
            if r["path"] == path:
                route["handler"] = r["handler"]
                route["params"] = r["params"]
                route["path"] = r["path"]
                return route
            # check if first part of route matches
            elif r["dynamic"] and matches(path, r["path"]):
                route = make_route(path, route, r)
                if route:
                    return route
        raise NotFound("Route not found")

    def __repr__(self) -> str:
        return f"<Pool method={self.method} routes={self.routes}>"
