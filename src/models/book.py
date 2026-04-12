from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Book:
    id: Optional[int] = None
    name: str = ""
    status: str = "available"
    quantity: int = 0
    issuedQuantity: int = 0
    availableCopies: int = 0 
    address: str = ""
    issuedBy: List[int] = field(default_factory=list) 
    defaulters: List[int] = field(default_factory=list)
    category: List[int] = field(default_factory=list)   