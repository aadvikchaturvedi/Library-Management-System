from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Library:
    id: Optional[int] = None
    name: str = ""
    address: str = ""
    staffMember: List[int] = field(default_factory=list)          
    books: List[int] = field(default_factory=list)             
    member: List[int] = field(default_factory=list)             
    transaction_history: List[int] = field(default_factory=list)