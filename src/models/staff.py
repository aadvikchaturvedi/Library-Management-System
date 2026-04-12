from dataclasses import dataclass
from typing import Optional

@dataclass
class Staff:
    id: Optional[int] = None
    name: str = ""
    age: int = 0
    gender: str = "M"
    role: str = ""