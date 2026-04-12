from dataclasses import dataclass
from typing import Optional

@dataclass
class Member:
    id: Optional[int] = None
    name: str = ""
    contactNumber: str = ""
    address: int = 0
    age: Optional[int] = None
    gender: str = "M" 
    penalty: Optional[int] = None 