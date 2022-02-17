import re
from sre_constants import MIN_UNTIL
from typing import List
from uuid import UUID
from radish.typings import Route, StoredRoute, WildCardVar
from pprint import pprint

var_types = {
    "int": int,
    "float": float,
    "str": str,
    "uuid": UUID,
}

def matches(path: str, regex) -> bool:
    match = re.match(regex, path, re.IGNORECASE)
    return match is not None



def make_route(path: str, stored_route: StoredRoute) -> dict | None:
    route: Route = {"path": path, "handler": None, "params": {}}
    matches = re.findall(stored_route["path"], path, re.IGNORECASE)

    # if matches[0] is tuple
    if isinstance(matches[0], tuple):
        # convert matches to list
        matches = list(matches[0])

    for i, var in enumerate(stored_route["vars"]):
        match = matches[i]
        typ = var_types[var.get("var_type") ]if var.get("var_type") else str
        route["params"]["{}".format(var["var"])] = typ(match)
    route["handler"] = stored_route["handler"]
    return route



def conv_wildcards(wildcard: dict) -> WildCardVar:
    return {"var": wildcard["wildcard"][1:], "var_type": "str", "extra": "wildcard"}


def triage(routes: List[Route]) -> Route:
    """
    This function will be used to determine which route to use
    """
    eva = {}
    for i, route in enumerate(routes):
        stored_route: StoredRoute = route.pop("stored_route")
        reg_path = stored_route["path"]
        segments = [s for s in reg_path.split("/") if s]
        eva[i] = len([seg for seg in segments if not seg.startswith("(?P") and not seg.endswith(")")])
    dt = {v: routes[k] for k, v in eva.items()}
    return dt[max(dt)]
    

   