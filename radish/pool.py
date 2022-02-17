from typing import Callable
import re
from typing import Any, Callable, List
from radish.exceptions import MethodNotAllowed, NotFound
from radish.typings import Route, StoredRoute, RoutingPriority
from radish.utils import make_route,  matches, conv_wildcards, triage
from pprint import pprint
__all__ = ["Pool"]


# regex for dynamic route parameters
dyn_regex = r"(\:(?P<var>[a-zA-Z]+)(?:\|(?P<var_type>[a-z]+))?)"
wld = r"(?P<wildcard>\*.*)"


class Pool(object):
    def __init__(self, method: str) -> None:
        self.method: str = method
        self.routes: List[StoredRoute] = []

    def insert(self, path: str, handler: Callable) -> None:
        route: StoredRoute = {"path": path,
                              "handler": handler, "vars": [], "params": {}}
        # check if route is dynamic
        route["dynamic"] = True if (":" in path or "*" in path) else False
        if route["dynamic"]:
            dyn_matches = [m.groupdict()
                           for m in re.finditer(dyn_regex, path, re.IGNORECASE)]
            wld_matches = [conv_wildcards(m.groupdict())
                           for m in re.finditer(wld, path, re.IGNORECASE)]
            variables = dyn_matches + wld_matches
            route["vars"] = variables
            for val in route["vars"]:
                # convert route to regex
                if val.get("extra") == "wildcard":
                    route["path"] = route["path"].replace("*" + val["var"], r"(?P<{}>.*)".format(val["var"]))
                else:
                    route["path"] = route["path"].replace(r":{}".format(
                        val['var']) if not val["var_type"] else r":{}|{}".format(val['var'],val['var_type'] ), r"(?P<{}>[^\/\?]+)".format(val['var']))
            return self.routes.append(route)
        else:
            return self.routes.append(route)

    def get(self, path: str) -> Route:
        routes: List = []
        for r in self.routes:
            if r["path"] == path and not r["dynamic"]:
                route: Route = {"path": path, "handler": None, "params": {}}
                route["handler"] = r["handler"]
                route["params"] = r["params"]
                route["path"] = r["path"]
                return route
            elif r["dynamic"] and matches(path, r["path"]):
                route = make_route(path, r)
                route["stored_route"] = r
                routes.append(route)
        if routes:
            if not len(routes) > 1:
                route = routes[0]
                route.pop("stored_route")
                print(route)
                return route
            else:
                route: Route = triage(routes)
                return route
        raise NotFound(f"Route {path} not found")

    def __repr__(self) -> str:
        return f"<Pool method={self.method} routes={self.routes}>"
