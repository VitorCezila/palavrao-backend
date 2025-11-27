from dataclasses import field
from typing import Optional

from attr import dataclass


@dataclass
class RequestContext:
    body: Optional[dict | str] = field(default=None)
    path_params: Optional[dict] = field(default=None)
    headers: Optional[dict] = field(default=None)
    path: Optional[str] = field(default=None)