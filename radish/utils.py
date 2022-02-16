import re
from typing import Any
from uuid import UUID
from radish.typings import Route, StoredRoute, WildCardVar
from radish.exceptions import DynamicError


var_types = {
    "int": int,
    "float": float,
    "str": str,
    "uuid": UUID,
}

def matches(path: str, regex) -> bool:
    return re.match(regex, path, re.IGNORECASE) is not None



def make_route(path: str, route: Route, stored_route: StoredRoute) -> Route | None:
    raw_matches = [m.groups() for m in re.finditer(stored_route["path"], path, re.IGNORECASE)]
    params: dict = {}
    matches: list = []
    if not raw_matches:
        return None
    if isinstance(raw_matches[0], tuple):
        for tup in raw_matches:
            for i in range(len(tup)):
                matches.append(tup[i])
    
    for i in zip(matches, stored_route ["vars"]):
        typ = var_types[i[1]["type"]] if i[1]["type"] else str
        params[i[1]["var"]] = typ(i[0])
    route["handler"] = stored_route["handler"]
    route["params"] = params
    route["path"] = path
    return route


def conv_wildcards(wildcard: dict) -> WildCardVar:
    return {"var": wildcard["wildcard"][1:], "var_type": "str", "extra": "wildcard"}