from collections import deque
from typing import (
    Dict,
    Deque,
    TypedDict
)


class Dispatcher(TypedDict):
    id: str
    status: str


dispatchers: Dict[TypedDict, Dispatcher] = {}
available_dispatchers: Deque = deque()
