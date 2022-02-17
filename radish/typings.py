from typing import Any, List, TypedDict, Callable
from enum import IntEnum

class Route(TypedDict):
    path: str
    handler: Callable
    params: dict

class Var(TypedDict):
    var_type: str
    var: str

class WildCardVar(Var):
    extra: str


class StoredRoute(TypedDict):
    vars: List[Var | WildCardVar] | None
    dynamic: bool
    path: str
    handler: Callable
    priority: "RoutingPriority"

class RoutingPriority(IntEnum):
    STATIC = 1
    DYNAMIC = 2
    WILDCARD = 3